
public class BlockedArrayAccessRacy extends Thread {

    static final int N = 10000000;
    static final int K = 2;

    static int a[] = new int[N];  

    int id;

    public BlockedArrayAccessRacy(int id) {
	this.id = id;
    }
    
    public void run() { 
	int start = N/K * id; 
	for (int i = 0; i < N/K; i++) {
	    a[start + i]=0;
	}
    }

    public static void main(String args[]) {	
	Thread t1 = new BlockedArrayAccessRacy(0);
	Thread t2 = new BlockedArrayAccessRacy(1);

	t1.start();  
	t2.start();  
	try {
	    t1.join();
	    //	    t2.join();  fail to join on t2
	} catch (InterruptedException e) {
	    System.exit(1);
	}

	// this loop races with t2 on a[N/2:N:1]
	for (int i = 0; i < N; i++) {
	    a[i] = 1; 
	}

    }
}


