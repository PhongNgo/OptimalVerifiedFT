
public class Worker extends Thread {

    int id;
    int a[];
    int start;
    int end;

    public Worker(int id, int a[], int start, int end) {
	this.id = id;  
	this.start = start;
	this.end = end;
	this.a = a;
    }
    
    public void run() { 
	for (int i = start; i < end; i++) {
	    a[i] = 0;  
	}
    }
}


