
public class BlockedArrayAccess extends Thread {

    static final int N = 10000000;
    static final int K = 4;

    static int a[] = new int[N];

    int id;

    public BlockedArrayAccess(int id) {
	this.id = id; 
    }
    
    public void run() { 
	int start = N/K * id;   
	for (int i = 0; i < N/K; i++) {
	    a[start + i]=0;    // [ReadShared Same Epoch] for a
	                       // [Write Exclusive] for a[start + i]
	}
    }

    public static void main(String args[]) {	
	Thread t1 = new BlockedArrayAccess(0);
	Thread t2 = new BlockedArrayAccess(1);
	Thread t3 = new BlockedArrayAccess(2);
	Thread t4 = new BlockedArrayAccess(3);

	/*
	 * Note: RoadRunner lazily initializes VarStates for
	 * object/array fields the first time they are accessed.  All
	 * checkers initialize both the last-read and last-write epoch
	 * for the VarState to be the accessing thread's current
	 * epoch, so that the very first access always hits a
	 * [... Same Epoch] case.  Thus, this initial write into a[i]
	 * counts as a [Write Same Epoch] case.
	 */
	for (int i = 0; i < N; i++) {
	    a[i] = 1;   // [Read Same Epoch] for a
                        // [Write Same Epoch] for a[i]

	}

	t1.start();  
	t2.start();  
	t3.start();
	t4.start();
	try {
	    t1.join();
	    t2.join();
	    t3.join();
	    t4.join();
	} catch (InterruptedException e) {
	    System.exit(1);
	}
	
	for (int i = 0; i < N; i++) {
	    a[i] = 1;   // [ReadShared Same Epoch] for a
	                // [Write Exclusive] for a[start + i]
	}
    }
}


