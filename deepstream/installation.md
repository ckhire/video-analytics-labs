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

         > tar xzvf Downloads/TensorRT-8.2.5.1.Linux.x86_64-gnu.cuda-11.4.cudnn8.2.tar.gz
         > export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/ckhire/TensorRT-8.2.5.1/lib
         > env | grep "LD_"
         > LD_LIBRARY_PATH=:/home/ckhire/TensorRT-8.2.5.1/lib
         > sudo pip3 install tensorrt-8.2.5.1-cp38-none-linux_x86_64.whl
         Processing ./tensorrt-8.2.5.1-cp38-none-linux_x86_64.whl
         Installing collected packages: tensorrt
         Successfully installed tensorrt-8.2.5.1
         > cd ../uff/
         > sudo pip3 install uff-0.6.9-py2.py3-none-any.whl
         Processing ./uff-0.6.9-py2.py3-none-any.whl
         Requirement already satisfied: protobuf>=3.3.0 in /usr/lib/python3/dist-packages (from uff==0.6.9) (3.6.1)
         Collecting numpy>=1.11.0
           Downloading numpy-1.24.4-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (17.3 MB)
              |████████████████████████████████| 17.3 MB 8.9 MB/s
         Installing collected packages: numpy, uff
         Successfully installed numpy-1.24.4 uff-0.6.9
         > cd ../graphsurgeon/
         > sudo pip3 install graphsurgeon-0.4.5-py2.py3-none-any.whl
         Processing ./graphsurgeon-0.4.5-py2.py3-none-any.whl
         Installing collected packages: graphsurgeon
         Successfully installed graphsurgeon-0.4.5

   e.  Installing lib Kafka

         > git clone https://github.com/edenhill/librdkafka.git
         > cd librdkafka
         > git reset --hard 7101c2310341ab3f4675fc565f64f0967e135a6a
         > ./configure
         checking for OS or distribution... ok (Ubuntu)
         checking for C compiler from CC env... failed
         checking for gcc (by command)... ok
         checking for C++ compiler from CXX env... failed
         checking for C++ compiler (g++)... ok
         checking executable ld... ok
         checking executable nm... ok
         checking executable objdump... ok
         checking executable strip... ok
         checking for pkgconfig (by command)... ok
         checking for install (by command)... ok
         checking for PIC (by compile)... ok
         checking for GNU-compatible linker options... ok
         checking for GNU linker-script ld flag... ok
         checking for __atomic_32 (by compile)... ok
         checking for __atomic_64 (by compile)... ok
         checking for socket (by compile)... ok
         parsing version '0x000b0401'... ok (0.11.4)
         checking for libpthread (by pkg-config)... failed
         checking for libpthread (by compile)... ok
         checking for zlib (by pkg-config)... ok
         checking for zlib (by compile)... ok (cached)
         checking for libcrypto (by pkg-config)... failed
         checking for libcrypto (by compile)... failed (disable)
         checking for liblz4 (by pkg-config)... failed
         checking for liblz4 (by compile)... failed (disable)
         checking for libssl (by pkg-config)... failed
         checking for libssl (by compile)... failed (disable)
         checking for libsasl2 (by pkg-config)... failed
         checking for libsasl2 (by compile)... failed (disable)
         checking for libsasl (by pkg-config)... failed
         checking for libsasl (by compile)... failed (disable)
         checking for crc32chw (by compile)... ok
         checking for regex (by compile)... ok
         checking for librt (by pkg-config)... failed
         checking for librt (by compile)... ok
         checking for strndup (by compile)... ok
         checking for strerror_r (by compile)... ok
         checking for libdl (by pkg-config)... failed
         checking for libdl (by compile)... ok
         checking for pthread_setname_gnu (by compile)... ok
         checking for nm (by env NM)... ok (cached)
         checking for python (by command)... failed (disable)
         disabling linker-script since python is not available
         Generated Makefile.config
         Generated config.h
         
         Configuration summary:
           prefix                   /usr/local
           ARCH                     x86_64
           CPU                      generic
           GEN_PKG_CONFIG           y
           ENABLE_DEVEL             n
           ENABLE_VALGRIND          n
           ENABLE_REFCNT_DEBUG      n
           ENABLE_SHAREDPTR_DEBUG   n
           ENABLE_LZ4_EXT           y
           ENABLE_SSL               y
           ENABLE_SASL              y
           MKL_APP_NAME             librdkafka
           MKL_APP_DESC_ONELINE     The Apache Kafka C/C++ library
           MKL_DISTRO               Ubuntu
           SOLIB_EXT                .so
           CC                       gcc
           CXX                      g++
           LD                       ld
           NM                       nm
           OBJDUMP                  objdump
           STRIP                    strip
           CPPFLAGS                 -g -O2 -fPIC -Wall -Wsign-compare -Wfloat-equal -Wpointer-arith -Wcast-align
           PKG_CONFIG               pkg-config
           INSTALL                  install
           LIB_LDFLAGS              -shared -Wl,-soname,$(LIBFILENAME)
           LDFLAG_LINKERSCRIPT      -Wl,--version-script=
           RDKAFKA_VERSION_STR      0.11.4
           MKL_APP_VERSION          0.11.4
           LIBS                     -lpthread -lz -lrt -ldl
           CFLAGS                   
           CXXFLAGS                 -Wno-non-virtual-dtor
           SYMDUMPER                $(NM) -D
           exec_prefix              /usr/local
           bindir                   /usr/local/bin
           sbindir                  /usr/local/sbin
           libexecdir               /usr/local/libexec
           datadir                  /usr/local/share
           sysconfdir               /usr/local/etc
           sharedstatedir           /usr/local/com
           localstatedir            /usr/local/var
           libdir                   /usr/local/lib
           includedir               /usr/local/include
           infodir                  /usr/local/info
           mandir                   /usr/local/man
         Generated config.cache

         > make
         make[1]: Entering directory '/home/ckhire/librdkafka/src'
         Creating shared library librdkafka.so.1
         gcc  -shared -Wl,-soname,librdkafka.so.1 rdkafka.o rdkafka_broker.o rdkafka_msg.o rdkafka_topic.o rdkafka_conf.o rdkafka_timer.o rdkafka_offset.o rdkafka_transport.o rdkafka_buf.o rdkafka_queue.o rdkafka_op.o rdkafka_request.o rdkafka_cgrp.o rdkafka_pattern.o rdkafka_partition.o rdkafka_subscription.o rdkafka_assignor.o rdkafka_range_assignor.o rdkafka_roundrobin_assignor.o rdkafka_feature.o rdcrc32.o crc32c.o rdmurmur2.o rdaddr.o rdrand.o rdlist.o tinycthread.o rdlog.o rdstring.o rdkafka_event.o rdkafka_metadata.o rdregex.o rdports.o rdkafka_metadata_cache.o rdavl.o rdkafka_sasl.o rdkafka_sasl_plain.o rdkafka_interceptor.o rdkafka_msgset_writer.o rdkafka_msgset_reader.o rdkafka_header.o rdvarint.o rdbuf.o rdunittest.o snappy.o rdgz.o rdkafka_lz4.o xxhash.o lz4.o lz4frame.o lz4hc.o rddl.o rdkafka_plugin.o -o librdkafka.so.1 -lpthread -lz -lrt -ldl
         Creating static library librdkafka.a
         ar rcs librdkafka.a rdkafka.o rdkafka_broker.o rdkafka_msg.o rdkafka_topic.o rdkafka_conf.o rdkafka_timer.o rdkafka_offset.o rdkafka_transport.o rdkafka_buf.o rdkafka_queue.o rdkafka_op.o rdkafka_request.o rdkafka_cgrp.o rdkafka_pattern.o rdkafka_partition.o rdkafka_subscription.o rdkafka_assignor.o rdkafka_range_assignor.o rdkafka_roundrobin_assignor.o rdkafka_feature.o rdcrc32.o crc32c.o rdmurmur2.o rdaddr.o rdrand.o rdlist.o tinycthread.o rdlog.o rdstring.o rdkafka_event.o rdkafka_metadata.o rdregex.o rdports.o rdkafka_metadata_cache.o rdavl.o rdkafka_sasl.o rdkafka_sasl_plain.o rdkafka_interceptor.o rdkafka_msgset_writer.o rdkafka_msgset_reader.o rdkafka_header.o rdvarint.o rdbuf.o rdunittest.o snappy.o rdgz.o rdkafka_lz4.o xxhash.o lz4.o lz4frame.o lz4hc.o rddl.o rdkafka_plugin.o
         Creating librdkafka.so symlink
         rm -f "librdkafka.so" && ln -s "librdkafka.so.1" "librdkafka.so"
         Generating pkg-config file rdkafka.pc
         Checking librdkafka integrity
         librdkafka.so.1                OK
         librdkafka.a                   OK
         Symbol visibility              OK
         make[1]: Leaving directory '/home/ckhire/librdkafka/src'
         make[1]: Entering directory '/home/ckhire/librdkafka/src-cpp'
         g++ -MD -MP -g -O2 -fPIC -Wall -Wsign-compare -Wfloat-equal -Wpointer-arith -Wcast-align -Wno-non-virtual-dtor -c RdKafka.cpp -o RdKafka.o
         g++ -MD -MP -g -O2 -fPIC -Wall -Wsign-compare -Wfloat-equal -Wpointer-arith -Wcast-align -Wno-non-virtual-dtor -c ConfImpl.cpp -o ConfImpl.o
         g++ -MD -MP -g -O2 -fPIC -Wall -Wsign-compare -Wfloat-equal -Wpointer-arith -Wcast-align -Wno-non-virtual-dtor -c HandleImpl.cpp -o HandleImpl.o
         g++ -MD -MP -g -O2 -fPIC -Wall -Wsign-compare -Wfloat-equal -Wpointer-arith -Wcast-align -Wno-non-virtual-dtor -c ConsumerImpl.cpp -o ConsumerImpl.o
         g++ -MD -MP -g -O2 -fPIC -Wall -Wsign-compare -Wfloat-equal -Wpointer-arith -Wcast-align -Wno-non-virtual-dtor -c ProducerImpl.cpp -o ProducerImpl.o
         g++ -MD -MP -g -O2 -fPIC -Wall -Wsign-compare -Wfloat-equal -Wpointer-arith -Wcast-align -Wno-non-virtual-dtor -c KafkaConsumerImpl.cpp -o KafkaConsumerImpl.o
         g++ -MD -MP -g -O2 -fPIC -Wall -Wsign-compare -Wfloat-equal -Wpointer-arith -Wcast-align -Wno-non-virtual-dtor -c TopicImpl.cpp -o TopicImpl.o
         g++ -MD -MP -g -O2 -fPIC -Wall -Wsign-compare -Wfloat-equal -Wpointer-arith -Wcast-align -Wno-non-virtual-dtor -c TopicPartitionImpl.cpp -o TopicPartitionImpl.o
         g++ -MD -MP -g -O2 -fPIC -Wall -Wsign-compare -Wfloat-equal -Wpointer-arith -Wcast-align -Wno-non-virtual-dtor -c MessageImpl.cpp -o MessageImpl.o
         g++ -MD -MP -g -O2 -fPIC -Wall -Wsign-compare -Wfloat-equal -Wpointer-arith -Wcast-align -Wno-non-virtual-dtor -c QueueImpl.cpp -o QueueImpl.o
         g++ -MD -MP -g -O2 -fPIC -Wall -Wsign-compare -Wfloat-equal -Wpointer-arith -Wcast-align -Wno-non-virtual-dtor -c MetadataImpl.cpp -o MetadataImpl.o
         Generating linker script librdkafka++.lds from rdkafkacpp.h
         Creating shared library librdkafka++.so.1
         gcc  -shared -Wl,-soname,librdkafka++.so.1 RdKafka.o ConfImpl.o HandleImpl.o ConsumerImpl.o ProducerImpl.o KafkaConsumerImpl.o TopicImpl.o TopicPartitionImpl.o MessageImpl.o QueueImpl.o MetadataImpl.o -o librdkafka++.so.1 -L../src -lrdkafka -lstdc++
         Creating static library librdkafka++.a
         ar rcs librdkafka++.a RdKafka.o ConfImpl.o HandleImpl.o ConsumerImpl.o ProducerImpl.o KafkaConsumerImpl.o TopicImpl.o TopicPartitionImpl.o MessageImpl.o QueueImpl.o MetadataImpl.o
         Creating librdkafka++.so symlink
         rm -f "librdkafka++.so" && ln -s "librdkafka++.so.1" "librdkafka++.so"
         Generating pkg-config file rdkafka++.pc
         Checking librdkafka++ integrity
         librdkafka++.so.1              OK
         librdkafka++.a                 OK
         make[1]: Leaving directory '/home/ckhire/librdkafka/src-cpp'
         make -C examples
         make[1]: Entering directory '/home/ckhire/librdkafka/examples'
         gcc -g -O2 -fPIC -Wall -Wsign-compare -Wfloat-equal -Wpointer-arith -Wcast-align  -I../src rdkafka_example.c -o rdkafka_example  \
         	../src/librdkafka.a -lpthread -lz -lrt -ldl
         # rdkafka_example is ready
         #
         # Run producer (write messages on stdin)
         ./rdkafka_example -P -t <topic> -p <partition>
         
         # or consumer
         ./rdkafka_example -C -t <topic> -p <partition>
         
         #
         # More usage options:
         ./rdkafka_example -h
         gcc -g -O2 -fPIC -Wall -Wsign-compare -Wfloat-equal -Wpointer-arith -Wcast-align  -I../src rdkafka_performance.c -o rdkafka_performance  \
         	../src/librdkafka.a -lpthread -lz -lrt -ldl
         # rdkafka_performance is ready
         #
         # Run producer
         ./rdkafka_performance -P -t <topic> -p <partition> -s <msgsize>
         
         # or consumer
         ./rdkafka_performance -C -t <topic> -p <partition>
         
         #
         # More usage options:
         ./rdkafka_performance -h
         g++ -g -O2 -fPIC -Wall -Wsign-compare -Wfloat-equal -Wpointer-arith -Wcast-align -Wno-non-virtual-dtor -I../src-cpp rdkafka_example.cpp -o rdkafka_example_cpp  \
         	../src-cpp/librdkafka++.a ../src/librdkafka.a -lpthread -lz -lrt -ldl -lstdc++
         gcc -g -O2 -fPIC -Wall -Wsign-compare -Wfloat-equal -Wpointer-arith -Wcast-align  -I../src rdkafka_consumer_example.c -o rdkafka_consumer_example  \
         	../src/librdkafka.a -lpthread -lz -lrt -ldl
         # rdkafka_consumer_example is ready
         #
         ./rdkafka_consumer_example <topic[:part]> <topic2[:part]> ..
         
         #
         # More usage options:
         ./rdkafka_consumer_example -h
         g++ -g -O2 -fPIC -Wall -Wsign-compare -Wfloat-equal -Wpointer-arith -Wcast-align -Wno-non-virtual-dtor -I../src-cpp rdkafka_consumer_example.cpp -o rdkafka_consumer_example_cpp  \
         	../src-cpp/librdkafka++.a ../src/librdkafka.a -lpthread -lz -lrt -ldl -lstdc++
         g++ -g -O2 -fPIC -Wall -Wsign-compare -Wfloat-equal -Wpointer-arith -Wcast-align -Wno-non-virtual-dtor -I../src-cpp kafkatest_verifiable_client.cpp -o kafkatest_verifiable_client  \
         	../src-cpp/librdkafka++.a ../src/librdkafka.a -lpthread -lz -lrt -ldl -lstdc++
         gcc -g -O2 -fPIC -Wall -Wsign-compare -Wfloat-equal -Wpointer-arith -Wcast-align  -I../src rdkafka_simple_producer.c -o rdkafka_simple_producer  \
         	../src/librdkafka.a -lpthread -lz -lrt -ldl
         make[1]: Leaving directory '/home/ckhire/librdkafka/examples'
         Updating
         CONFIGURATION.md CONFIGURATION.md.tmp differ: byte 345, line 6
         Checking  integrity
         CONFIGURATION.md               OK
         examples/rdkafka_example       OK
         examples/rdkafka_performance   OK
         examples/rdkafka_example_cpp   OK
         make[1]: Entering directory '/home/ckhire/librdkafka/src'
         Checking librdkafka integrity
         librdkafka.so.1                OK
         librdkafka.a                   OK
         Symbol visibility              OK
         make[1]: Leaving directory '/home/ckhire/librdkafka/src'
         make[1]: Entering directory '/home/ckhire/librdkafka/src-cpp'
         Checking librdkafka++ integrity
         librdkafka++.so.1              OK
         librdkafka++.a                 OK
         make[1]: Leaving directory '/home/ckhire/librdkafka/src-cpp'

         > sudo make install
            make[1]: Entering directory '/home/ckhire/librdkafka/src'
         Install librdkafka to /usr/local
         install -d $DESTDIR/usr/local/include/librdkafka ; \
         install -d $DESTDIR/usr/local/lib ; \
         install rdkafka.h $DESTDIR/usr/local/include/librdkafka ; \
         install librdkafka.a $DESTDIR/usr/local/lib ; \
         install librdkafka.so.1 $DESTDIR/usr/local/lib ; \
         [ -f "rdkafka.pc" ] && ( \
         	install -d $DESTDIR/usr/local/lib/pkgconfig ; \
         	install -m 0644 rdkafka.pc $DESTDIR/usr/local/lib/pkgconfig \
         ) ; \
         (cd $DESTDIR/usr/local/lib && ln -sf librdkafka.so.1 librdkafka.so)
         make[1]: Leaving directory '/home/ckhire/librdkafka/src'
         make[1]: Entering directory '/home/ckhire/librdkafka/src-cpp'
         Install librdkafka++ to /usr/local
         install -d $DESTDIR/usr/local/include/librdkafka ; \
         install -d $DESTDIR/usr/local/lib ; \
         install rdkafkacpp.h $DESTDIR/usr/local/include/librdkafka ; \
         install librdkafka++.a $DESTDIR/usr/local/lib ; \
         install librdkafka++.so.1 $DESTDIR/usr/local/lib ; \
         [ -f "rdkafka++.pc" ] && ( \
         	install -d $DESTDIR/usr/local/lib/pkgconfig ; \
         	install -m 0644 rdkafka++.pc $DESTDIR/usr/local/lib/pkgconfig \
         ) ; \
         (cd $DESTDIR/usr/local/lib && ln -sf librdkafka++.so.1 librdkafka++.so)
         make[1]: Leaving directory '/home/ckhire/librdkafka/src-cpp'

   f.  Install Deepstream 6.1

         > 

       









   
   
   
