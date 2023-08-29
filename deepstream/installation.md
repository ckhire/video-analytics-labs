Aug 27 I brought new laptop Asus TUF F15 2023. I installed Ubuntu 20.04.6. I want to take this chance to list all the steps of installing various packages required for configuring the Development Machine for Deep Learning in Computer Vision Domain

## Deepstream 6.1 SDK 

1. ### System Reequirements
   a. RTX 3050 4GB mobile card<br>
   b. Ubuntu 20.04.6<br>
   c. GStreamer 1.16.2<br>
   d. NVIDIA driver 510.47.03<br>
   e. CUDA 11.6 Update 1<br>
   f. TensorRT 8.2.5.1<br>

2. ### Start the Process
   Since this OS is newly installed and I don't have any previous attempt of installing the G-Streamer. I will skip first of removing the previous DeepStream installation  

   a.  **Install Dependencies**
            
         sudo apt install \
          libssl1.1 \
          libgstreamer1.0-0 \
          gstreamer1.0-tools \
          gstreamer1.0-plugins-good \
          gstreamer1.0-plugins-bad \
          gstreamer1.0-plugins-ugly \
          gstreamer1.0-libav \
          libgstrtspserver-1.0-0 \
          libjansson4 \
          libyaml-cpp-dev \
          gcc \
          make \
          git \
          python3
        ```

   b.  NVIDIA driver installation on ubuntu. I tried the way it was mentioned in the documentation but it fails. Now I will try through ubuntu software center.
       I followed below steps for installation from [here](https://phoenixnap.com/kb/install-nvidia-drivers-ubuntu)

        > sudo apt update
        > sudo apt upgrade
        > sudo add-apt-repository ppa:graphics-drivers/ppa
        > ubuntu-drivers devices
        > sudo apt install nvidia-driver-525

    c.  Installing CUDA through NVIDIA's website rather than through ubuntu command <br>
      
        > wget https://developer.download.nvidia.com/compute/cuda/11.6.1/local_installers/cuda_11.6.1_510.47.03_linux.run
        > sudo sh cuda_11.6.1_510.47.03_linux.run
        # Verify the installation. The output is as below
          = Summary =
          ===========
          
          Driver:   Not Selected
          Toolkit:  Installed in /usr/local/cuda-11.6/
          
          Please make sure that
           -   PATH includes /usr/local/cuda-11.6/bin
           -   LD_LIBRARY_PATH includes /usr/local/cuda-11.6/lib64, or, add /usr/local/cuda-11.6/lib64 to /etc/ld.so.conf and run ldconfig as root
          
          To uninstall the CUDA Toolkit, run cuda-uninstaller in /usr/local/cuda-11.6/bin
          ***WARNING: Incomplete installation! This installation did not install the CUDA Driver. A driver of version at least 510.00 is required for CUDA 11.6 functionality to work.
          To install the driver using this installer, run the following command, replacing <CudaInstaller> with the name of this run file:
              sudo <CudaInstaller>.run --silent --driver
         > tail /var/log/cuda-installer.log
         > [INFO]: Installed: /usr/local/cuda-11.6/extras/demo_suite/randomFog
          [WARNING]: Cannot find manpages to install.
          [INFO]: CUDA Documentation 11.6
          [INFO]: Successfully created directory: /usr/local/cuda-11.6/tools
          [INFO]: Installed: /usr/local/cuda-11.6/DOCS
          [INFO]: Installed: /usr/local/cuda-11.6/EULA.txt
          [INFO]: Installed: /usr/local/cuda-11.6/README
          [INFO]: Skipping copy. File already exists at: /usr/local/cuda-11.6/bin/cuda-uninstaller
          [INFO]: Installed: /usr/local/cuda-11.6/tools/CUDA_Occupancy_Calculator.xls
          [WARNING]: Cannot find manpages to install.
      
     d.   Install TensorRT 8.2.5.1



   
   
   
