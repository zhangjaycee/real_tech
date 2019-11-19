# 内核线程 kthread

类比pthread，kthread近似功能的函数：

|pthread|kthread|
|-|-|
|pthread_t|task_struct|
|pthread_create|kthread_run/kthread_create|
|pthread_exit|kthread_should_stop|
|pthread_join|kthread_stop|



---
[1] 《深入理解并行编程》

[2] http://www.cs.fsu.edu/~cop4610t/lectures/project2/kthreads/kthreads.pdf