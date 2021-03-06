?	;?5Y?Zx@;?5Y?Zx@!;?5Y?Zx@      ??!       "?
=type.googleapis.com/tensorflow.profiler.PerGenericStepDetailsC;?5Y?Zx@$????_s@1??+??tG@A????&M??I>?h??_@@rEagerKernelExecute 0*	??C?\??@2~
GIterator::Model::MaxIntraOpParallelism::Prefetch::FlatMap[0]::Generator}	^(.@!?_d??X@)}	^(.@1?_d??X@:Preprocessing2g
0Iterator::Model::MaxIntraOpParallelism::Prefetch6;R}???!?6ޯ?.??)6;R}???1?6ޯ?.??:Preprocessing2]
&Iterator::Model::MaxIntraOpParallelism??L?Nϳ?!=?J?T??)+??O8???1???C???:Preprocessing2F
Iterator::Modelo?[t???!??Zp???)G仔?dl?1?Z?Dh??:Preprocessing2p
9Iterator::Model::MaxIntraOpParallelism::Prefetch::FlatMapR???).@!?J??X@)?V횐?h?1???>?y??:Preprocessing:?
]Enqueuing data: you may want to combine small input data chunks into fewer but larger chunks.
?Data preprocessing: you may increase num_parallel_calls in <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#map" target="_blank">Dataset map()</a> or preprocess the data OFFLINE.
?Reading data from files in advance: you may tune parameters in the following tf.data API (<a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#prefetch" target="_blank">prefetch size</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#interleave" target="_blank">interleave cycle_length</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset#class_tfrecorddataset" target="_blank">reader buffer_size</a>)
?Reading data from files on demand: you should read data IN ADVANCE using the following tf.data API (<a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#prefetch" target="_blank">prefetch</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#interleave" target="_blank">interleave</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset#class_tfrecorddataset" target="_blank">reader buffer</a>)
?Other data reading or processing: you may consider using the <a href="https://www.tensorflow.org/programmers_guide/datasets" target="_blank">tf.data API</a> (if you are not using it now)?
:type.googleapis.com/tensorflow.profiler.BottleneckAnalysis?
both?Your program is POTENTIALLY input-bound because 79.5% of the total step time sampled is spent on 'All Others' time (which could be due to I/O or Python execution or both).moderate"?8.4 % of the total step time sampled is spent on 'Kernel Launch'. It could be due to CPU contention with tf.data. In this case, you may try to set the environment variable TF_GPU_THREAD_MODE=gpu_private.*noI???U@Q??ϗ(@Zno>Look at Section 3 for the breakdown of input time on the host.B?
@type.googleapis.com/tensorflow.profiler.GenericStepTimeBreakdown?
	$????_s@$????_s@!$????_s@      ??!       "	??+??tG@??+??tG@!??+??tG@*      ??!       2	????&M??????&M??!????&M??:	>?h??_@@>?h??_@@!>?h??_@@B      ??!       J      ??!       R      ??!       Z      ??!       b      ??!       JGPUb q???U@y??ϗ(@?"-
IteratorGetNext/_4_Recvl???!??!l???!??"-
IteratorGetNext/_2_Recv?????m??!z?ia?G??"-
IteratorGetNext/_6_Recv5J??!J??!ʜ^,m???"@
$model_12/FinRecoModel/conv3/Conv2D_2Conv2Dl?vָ??!?1?????"@
"model_12/FinRecoModel/conv3/Conv2DConv2D??^I???!??+????0"@
$model_12/FinRecoModel/conv3/Conv2D_1Conv2D+~?'????!???ĕ??"?
Wgradient_tape/model_12/FinRecoModel/inception_3c_3x3_conv2/Conv2D_1/Conv2DBackpropInputConv2DBackpropInput?T??N???!I???????0"?
Ugradient_tape/model_12/FinRecoModel/inception_3c_3x3_conv2/Conv2D/Conv2DBackpropInputConv2DBackpropInput??j??Y??!?W?,6??0"?
Wgradient_tape/model_12/FinRecoModel/inception_3c_3x3_conv2/Conv2D_2/Conv2DBackpropInputConv2DBackpropInputb?K?E??!fKP&h???0"?
Xgradient_tape/model_12/FinRecoModel/inception_3c_3x3_conv1/Conv2D_2/Conv2DBackpropFilterConv2DBackpropFilter?ao!??}?!s?[?/??0Q      Y@Y????
&??aF???X@q??8??T@y?µ?x???"?
both?Your program is POTENTIALLY input-bound because 79.5% of the total step time sampled is spent on 'All Others' time (which could be due to I/O or Python execution or both).b
`input_pipeline_analyzer (especially Section 3 for the breakdown of input operations on the Host)Q
Otf_data_bottleneck_analysis (find the bottleneck in the tf.data input pipeline)m
ktrace_viewer (look at the activities on the timeline of each Host Thread near the bottom of the trace view)"O
Mtensorflow_stats (identify the time-consuming operations executed on the GPU)"U
Strace_viewer (look at the activities on the timeline of each GPU in the trace view)*?
?<a href="https://www.tensorflow.org/guide/data_performance_analysis" target="_blank">Analyze tf.data performance with the TF Profiler</a>*y
w<a href="https://www.tensorflow.org/guide/data_performance" target="_blank">Better performance with the tf.data API</a>2?
=type.googleapis.com/tensorflow.profiler.GenericRecommendation?
moderate?8.4 % of the total step time sampled is spent on 'Kernel Launch'. It could be due to CPU contention with tf.data. In this case, you may try to set the environment variable TF_GPU_THREAD_MODE=gpu_private.no*?Only 0.0% of device computation is 16 bit. So you might want to replace more 32-bit Ops by 16-bit Ops to improve performance (if the reduced accuracy is acceptable).2no:
Refer to the TF2 Profiler FAQb?84.0% of Op time on the host used eager execution. Performance could be improved with <a href="https://www.tensorflow.org/guide/function" target="_blank">tf.function.</a>2"Nvidia GPU (Turing)(: B 