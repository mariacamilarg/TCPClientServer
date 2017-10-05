import java.io.IOException;
import java.net.ServerSocket;

public class Servidor {
	
	private static final int PUERTO = 8080;
	
	public static void main(String[] args) throws IOException {
		
		ServerSocket ss = null;
		boolean continuar = true;
		int idThreadServidor = 0;
		
		try {
			ss = new ServerSocket(PUERTO);
		} 
		catch (IOException e) {
			System.err.println("No pudo crear socket en el puerto:" + PUERTO);
			System.exit(-1);
		}
		
		while (continuar) {
			ThreadServidor delegado = new ThreadServidor(ss.accept(), idThreadServidor);
			delegado.start();
			idThreadServidor++;
		}
		
		ss.close();
	}
	
}
