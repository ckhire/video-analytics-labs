## Index
	1. Introduction
	2. Functions under consideration
	3. Analysis of the CPU functions
	4. GPU Kernels
	5. Latency on GPU vs CPU
	6. Memory Management on GPU
	7. Kernel Integration with SYNC API
	8. Kernel Integration with ASYNC API
	9. Better ways of Optimizing the SYNC and ASYNC API


### 1. Introduction

 This document is about the details of CPU operations which are taking more latency and meomory. These operations are related to Pre-processing part of the image. The pre-processing comprises of two important operations:
i. `preprocess_img` function on CPU
ii. Normalization operations on the result of above

In this document the details like the latency on CPU and GPU, GPU memory consumption of the kernels, various ways to integrate the kernels with the existing API and better GPU Memory Management is addressed.

### 2. Functions under consideration

Here is the detail CPU code for both of the above steps mentioned.

i. `preprocess_img` function

```cpp
cv::Mat preprocess_img(cv::Mat& img, int INPUT_H, int INPUT_W)
{
    int w, h, x, y;
    float r_w = INPUT_W / (img.cols * 1.0);
    float r_h = INPUT_H / (img.rows * 1.0);
    if (r_h > r_w)
    {
        w = INPUT_W;
        h = r_w * img.rows;
        x = 0;
        y = (INPUT_H - h) / 2;
    }
    else
    {
        w = r_h * img.cols;
        h = INPUT_H;
        x = (INPUT_W - w) / 2;
        y = 0;
    }
    cv::Mat re(h, w, CV_8UC3);
    cv::resize(img, re, re.size(), 0, 0, cv::INTER_LINEAR);
    cv::Mat out(INPUT_H, INPUT_W, CV_8UC3, cv::Scalar(128, 128, 128));
    re.copyTo(out(cv::Rect(x, y, re.cols, re.rows)));
    return re;
}
```

ii. Normalization on above result

```cpp
float* create_input_tensor_from_image(cv::Mat& img, float data[]) {
    
    for (int i = 0; i < INPUT_H * INPUT_W; i++)
    {

        
        data[ i] = (float)img.at<cv::Vec3b>(i)[2] / 255.0;
       
        data[i + INPUT_H * INPUT_W] = (float)img.at<cv::Vec3b>(i)[1] / 255.0;
        
        data[ i + 2 * INPUT_H * INPUT_W] = (float)img.at<cv::Vec3b>(i)[0] / 255.0;
       
    }
    
    return data;
}
```

### 3. Analysis of the CPU functions

1. `preprocess_img` In this function the critical steps consuming the memory and more CPU time are:
    1. Creating two empty Mat with different size
    2. Resizing the input Mat and saving it to one of the empty Mat created earlier
    3. Copying the resize Mat to another larger empty Mat which is created earlier.

    The major issue of this algorithm is that in every iteration i.e for every frame it creates 2 empty Mat and performs resize and then recopy the resize Mat to another larger empty Mat. Thus while performing this operation there happens to be 3 Mats in the Memory. 

     #### Optimization Scope
     1. Most important thing to notice is that the `out` Mat could be created at the load time itself. Thus avoiding the time to create it in every iteration.
     2. From the above steps it is clear that finally the resize Mat should be saved in larger Mat. As it is clear from above function that the __x__ , __y__ of the larger Mat are known only after following the `if-else` block. Thus it is possible to save the resize Mat directly in the larger Mat immediately after knowing the __x__, __y__ values.
     3. This way the resize operation is sufficent to do all three steps of the above CPU function. This will reduce the Memory because now there will be only 2 Mats in the system.
     4. The size of the larger Mat is already known in advance to us. Thus this Mat could be allocated on CUDA at the time of loading the inference engine. This will save larger time of cuda memory allocation and won't be repetative. Since the copying is done on the same location a clean operation could be perform before saving the resize result. In clean operation one can clean the location by saving `128` value as pixel values. This is very fast operation and won't take more than 10-15 micro-seconds.

2.  `create_input_tensor_from_image` In this function now there is another buffer memory other than the final resize Mat. This memory is necessary because Mat is actually not continuous. Thus the normalization is actually enssuring that the memory is continuous and normalized both at once.
    1. This function is already in single for loop. Not much scope is here to optimize it other than just having it on GPU kernel.


### 4. GPU Kernels

1. For  `preprocess_img` I have divided this into two parts the decision of width > height  and other will be accomplished on CPU only. Rest everyting is done in single steps by `preprocessUsingCudaNPP` function. Now this is not actually the cuda kernel but the Npp function is as wrapper over the kernel. Thus it would be consider like-wise to avoid any further confusion while scheduling it.
2. For `create_input_tensor_from_image` I have created `channel_normalization_3c` cuda kernel. Currently there is another continuous GPU buffere as equivalent to that of `data`.
**Note: This actually could be done on the same Mat which is received from the above step. So this operation could be done in-place. But for this the kernel should be tested with multiple image sizes.**
 
### 5. Latency on GPU vs CPU


| Cuda Function  | Function Description | Time in Micro seconds | Input Frame Size | CPU Function | Time in microseconds for CPU |
|------------------|------------------------|--------------------------|--------------------|-----|------------------------------|
| preprocessUsingCudaNPP       |  Image Pre-processing steps including resize maintaining aspect ratio and copying to new Mat | 373. 18 | 1920 x 1080 | `preprocess_img` | 1500 |
| channel_normalization_3c | CPU Channel normalization post-pre-processing | 449.22 | YOLO adjusted ASPECT | `create_input_tensor_from_image` | 1700 |
| preprocessUsingCudaNPP       |  Image Pre-processing steps including resize maintaining aspect ratio and copying to new Mat | 51.492 | 650 x 480 |`preprocess_img` | 1000 |
| channel_normalization_3c | CPU Channel normalization post-pre-processing | 495.05 | YOLO adjusted ASPECT | `create_input_tensor_from_image` | 1000 |

**Preliminary Conclusion : On CPU total time needed is ~3.2 ms and on GPU it is ~ 0.8 ms.**

### 6. Memory Management on GPU

 As explained above at the time of inference model loading we could allocated the memory for the final buffer. As per current assumption we would need two memory spaces on GPU. One to save the result of the `preprocessUsingCudaNPP` and another to do save normalization result.
Now with every new frame we would be just copying data from CPU to our location and both kernels would be performin operations on same location. This is considering that the every frame is already on GPU. This is possible. In case this is not there then also the above results are comparable because in above case also we are copying the final normalized buffer to GPU in every iteration. Comparable to this another Mat for the input frame on GPU could be pre-allocated at the time of loading and then only Mat copying from CPU to GPU will take place. Thus both the things are well comparable.
In lateral case as stated in prior statement the second CPU to GPU won't happen. Rather only once CPU to GPU of orignal MAT will take place and later everything is on GPU and with one MAT less as compare to CPU. Further if the second kernel could be perform safely in-place then we would need only 2 Mat's on GPU and second Mat could serve as it is to the inferencing function.
Here the two Mats are spoken in terms of having there management on the `core` side. Otherwise if GPU decoding is in picture the first Mat will be already available on GPU.


### 7. Kernel Integration with SYNC API

For sync API following things would be go under drasctic changes:
1. Existing Loader would need to know the amount of GPU available and how many variables could be allocated on it.
2. If the image is not on GPU after decoding then image Mat and the final Mat should be allocated on the GPU while loading the engine.
3. Knowledge of various variables avaialble on GPU along with its pointers should be known to some central loader
4. New API needs to be exposed to allow copying of Mat from CPU to GPU in particualr strucutre.
5. Another version of SYNC API would be needed which will take the new strucutre and would pass it to the new functions which would internally give calls to above 2 kernels
6. The new SYNC API would have different wiring and internal functions as compared to the existing YOLOv5.
7. This is needed because all the steps of GPU will post it resultant pointer to the inference function which would then infere on GPU only.
8. Inferencing logic needs to check for various profiled base inferencing technique as provided by the tensorrt to circumvate the passing of pointers.
9. Later on rest would be same as that of current SYNC version
10. For batch base inferencing there would be more handling around queue of the GPU. Some of this part will get covered in ASYNC version
11. Underline function would be of batching.

### 8. Kernel Integration with ASYNC API
Implementation of Asyc API is more complex than the current ASYNC API:
1. Creating the Multilevel Queue on Cuda with custom strucutres
2. Creating the shared strucutral Queue elements pointing to varies location on CUDA
3. Managing both the above aspects of the Queue
4. Wrapping the kernel using dedicated threads to use particular locations to perform the kernel operations over it.
5. Implementing observation base threads to utilize the GPU memory in faster way and to reduce signal timing between threads
6. In Async the pre-processing kernel will get free in ~500 micro-seconds for one frame and thus using 2 such kernels would be able to address 10 streams sequential in 2.5 milli-seconds
7. Similarly 2 sets of normalization kernel would address all the 10 streams in 1 milliseconds.
8. Similarly 2 sets of inference engine would take ~8 ms to produce 2 sets of detections on 2 images.
9. Similary 2 sets of nms would be needed so that the inference on completing there job will go on infering other normalized pre-processed frames.
10. To handle above on GPU the complete model and new design would be implemented.
11. Moreover these queue's would be global to the particualr loader thus common to all the kernels. But the API needs to be implemented in Observer Visitor Pattern with multiple threads. This is itself research base desings
12. Thus this new API would be more complex and require many other modules to explicitly schedules the intermediate results on particular kernels without wasting time in wait-signal model


### 9. Better ways of Optimizing the SYNC and ASYNC API

Approach I: This is already covered in above case.

Approach II: To have the knowledge of input frame properties like width and height before loading the model and then to allocate memory while loading the models. As soon as the frame is read by using current decoding i.e ffmpeg the CPU to GPU Mat copying should get started using particular structure which would be define in Core and expose as API.

Approach III: In case we decide to use the GPU base decoding then we will be saving enormous time because the intedend size frame would get directly saved in Core custom structure and then to the API directly. Thus the cuda copying and pre-processing would be handle immediately post decoding. In short the decoded frame would be normalized and could be given to the inferencing. With this approach the frame reading itself would do normalized pre-processing thus there would be only toll of inferencing and post-processing saving enormous time

Approach IV: End-to-End development as GStream pipeline. This will need integration of Core with GStream API and every other component would be additional plugin to be used in Pipline pardigm architecture. The would be more beneficial as the end-to-end cycle is nothing but stage in pipeline and the load scheduling, frame scheduling and multithreading of streams would be taken care internally by the framework. This approach needs more research and Study. This is equivalent to developing the Core API like Big Data Pipeline where there could be multiple streams as input and bulk output.