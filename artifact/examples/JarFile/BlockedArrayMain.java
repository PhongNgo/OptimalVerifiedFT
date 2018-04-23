public class BlockedArrayMain {

    static final int K = 4;
    static final int W = 2500000;
    static final int N = K * W
;
    static int a[] = new int[N];  // access a, check a.

    public static void main(String args[]) {	
	Worker[] ws = new Worker[K];

	for (int i = 0; i < K; i++) {
	    ws[i] = new Worker(i, a, i*W, (i+1)*W);
	}

	for (int i = 0; i < K; i++) {
	    ws[i].start();
	}

	try {
	    for (int i = 0; i < K; i++) {
		ws[i].join();
	    }
	} catch (InterruptedException e) {
	    System.exit(1);
	}
	
	for (int i = 0; i < N; i++) {
	    a[i] = 1;  
	}
    }
}


