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
          Here as you see I followed lot of steps from DeepStream documentation to install tensorrt. But as it is evident in the last step it is trying to install few cuda 12 packages. It sometimes give issues.
          Thus I will install required tensort version from tar file.
   
         > sudo rm /etc/apt/sources.list.d/*cuda*
         rm: cannot remove '/etc/apt/sources.list.d/*cuda*': No such file or directory
         > sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
         Executing: /tmp/apt-key-gpghome.YFT0jSCJhL/gpg.1.sh --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
         gpg: requesting key from 'https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub'
         gpg: key A4B469963BF863CC: public key "cudatools <cudatools@nvidia.com>" imported
         gpg: Total number processed: 1
         gpg:               imported: 1
         > sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
         > sudo apt-get update
         # Download cudnn 8.4.0 and 11.x local repo packages
         > sudo dpkg -i cudnn-local-repo-ubuntu2004-8.4.0.27_1.0-1_amd64.deb
         Selecting previously unselected package cudnn-local-repo-ubuntu2004-8.4.0.27.
         (Reading database ... 188182 files and directories currently installed.)
         Preparing to unpack cudnn-local-repo-ubuntu2004-8.4.0.27_1.0-1_amd64.deb ...
         Unpacking cudnn-local-repo-ubuntu2004-8.4.0.27 (1.0-1) ...
         Setting up cudnn-local-repo-ubuntu2004-8.4.0.27 (1.0-1) ...
         
         The public CUDA GPG key does not appear to be installed.
         To install the key, run this command:
         sudo apt-key add /var/cudnn-local-repo-ubuntu2004-8.4.0.27/7fa2af80.pub
         > sudo apt-get update
         Reading package lists... Done
         W: GPG error: file:/var/cudnn-local-repo-ubuntu2004-8.4.0.27  Release: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY F60F4B3D7FA2AF80
         E: The repository 'file:/var/cudnn-local-repo-ubuntu2004-8.4.0.27  Release' is not signed.
         N: Updating from such a repository can't be done securely, and is therefore disabled by default.
         N: See apt-secure(8) manpage for repository creation and user configuration details.
         > sudo apt install libcudnn8=8.4.0.27-1+cuda11.6 libcudnn8-dev=8.4.0.27-1+cuda11.6
         The following NEW packages will be installed:
           libcudnn8 libcudnn8-dev
         0 upgraded, 2 newly installed, 0 to remove and 23 not upgraded.
         > sudo dpkg -i nv-tensorrt-repo-ubuntu2004-cuda11.4-trt8.2.5.1-ga-20220505_1-1_amd64.deb
            Selecting previously unselected package nv-tensorrt-repo-ubuntu2004-cuda11.4-trt8.2.5.1-ga-20220505.
            (Reading database ... 188244 files and directories currently installed.)
            Preparing to unpack nv-tensorrt-repo-ubuntu2004-cuda11.4-trt8.2.5.1-ga-20220505_1-1_amd64.deb ...
            Unpacking nv-tensorrt-repo-ubuntu2004-cuda11.4-trt8.2.5.1-ga-20220505 (1-1) ...
            Setting up nv-tensorrt-repo-ubuntu2004-cuda11.4-trt8.2.5.1-ga-20220505 (1-1) ...
            
            The public CUDA GPG key does not appear to be installed.
            To install the key, run this command:
            sudo apt-key add /var/nv-tensorrt-repo-ubuntu2004-cuda11.4-trt8.2.5.1-ga-20220505/82307095.pub
         > sudo apt-key add /var/nv-tensorrt-repo-ubuntu2004-cuda11.4-trt8.2.5.1-ga-20220505/82307095.pub
            OK
         > sudo apt-get update
            Reading package lists... Done
         W: GPG error: file:/var/cudnn-local-repo-ubuntu2004-8.4.0.27  Release: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY F60F4B3D7FA2AF80
         E: The repository 'file:/var/cudnn-local-repo-ubuntu2004-8.4.0.27  Release' is not signed.
         N: Updating from such a repository can't be done securely, and is therefore disabled by default.
         N: See apt-secure(8) manpage for repository creation and user configuration details.

         >  sudo apt install tensorrt
         Reading package lists... Done
         Building dependency tree       
         Reading state information... Done
         The following additional packages will be installed:
           cuda-cccl-12-1 cuda-cccl-12-2 cuda-cudart-12-1 cuda-cudart-12-2 cuda-cudart-dev-12-1 cuda-cudart-dev-12-2 cuda-driver-dev-12-1 cuda-driver-dev-12-2 cuda-nvcc-12-1 cuda-toolkit-12-1-config-common
           cuda-toolkit-12-2-config-common cuda-toolkit-12-config-common cuda-toolkit-config-common libcublas-12-2 libcublas-dev-12-2 libnvinfer-bin libnvinfer-dev libnvinfer-dispatch-dev libnvinfer-dispatch8
           libnvinfer-headers-dev libnvinfer-headers-plugin-dev libnvinfer-lean-dev libnvinfer-lean8 libnvinfer-plugin-dev libnvinfer-plugin8 libnvinfer-samples libnvinfer-vc-plugin-dev libnvinfer-vc-plugin8
           libnvinfer8 libnvonnxparsers-dev libnvonnxparsers8 libnvparsers-dev libnvparsers8
         The following NEW packages will be installed:
           cuda-cccl-12-1 cuda-cccl-12-2 cuda-cudart-12-1 cuda-cudart-12-2 cuda-cudart-dev-12-1 cuda-cudart-dev-12-2 cuda-driver-dev-12-1 cuda-driver-dev-12-2 cuda-nvcc-12-1 cuda-toolkit-12-1-config-common
           cuda-toolkit-12-2-config-common cuda-toolkit-12-config-common cuda-toolkit-config-common libcublas-12-2 libcublas-dev-12-2 libnvinfer-bin libnvinfer-dev libnvinfer-dispatch-dev libnvinfer-dispatch8
           libnvinfer-headers-dev libnvinfer-headers-plugin-dev libnvinfer-lean-dev libnvinfer-lean8 libnvinfer-plugin-dev libnvinfer-plugin8 libnvinfer-samples libnvinfer-vc-plugin-dev libnvinfer-vc-plugin8
           libnvinfer8 libnvonnxparsers-dev libnvonnxparsers8 libnvparsers-dev libnvparsers8 tensorrt
         0 upgraded, 34 newly installed, 0 to remove and 25 not upgraded.
         Need to get 2,058 MB of archives.
         After this operation, 5,540 MB of additional disk space will be used.
         Do you want to continue? [Y/n] n
         Abort.

      Installing Tensorrt 8.2.5.1 using tar file
   






   
   
   
