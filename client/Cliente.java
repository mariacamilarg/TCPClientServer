import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class Cliente {
	
	public static final String IP = "169.254.156.87";
	private static final int PUERTO = 8080;
	
	public static void main(String[] args) throws IOException {
		
		Socket socket;
		PrintWriter escritor;
		BufferedReader lector;
		
		try {
			socket = new Socket(IP, PUERTO);
			
			escritor = new PrintWriter(socket.getOutputStream(), true);
			lector = new BufferedReader(new InputStreamReader(socket.getInputStream()));
			
			procesar(lector, escritor);
			
			socket.close();
			escritor.close();
			lector.close();
		} 
		catch (Exception e) {
			System.err.println("Exception: " + e.getMessage());
			System.exit(1);
		}
	}
	
	public static void procesar(BufferedReader pIn, PrintWriter pOut) throws IOException {
		
		BufferedReader stdIn = new BufferedReader(new InputStreamReader(System.in));
		
		String inputLine, outputLine;
		int estado = 0;
		boolean ejecutar = true;
		
		System.out.print("Inicie la comunicación con HOLA (ponga OK si quiere terminarla):");
		outputLine = stdIn.readLine();
		System.out.println("Cliente: " + outputLine);
		if (outputLine.equalsIgnoreCase("OK")){
			estado = 2;
			ejecutar = false;
		}
		pOut.println(outputLine);
		
		while(ejecutar){

			//TODO: CAMBIAR ESTOOOOOO
			
			inputLine = pIn.readLine();
			System.out.println("Cliente (esto me dijo el servidor)"+inputLine);
			
			while (estado < 2 && (inputLine != null) ) {
				switch (estado) {
					case 0:
						if (inputLine.equalsIgnoreCase("LISTO")) {
							System.out.print("Escriba el mensaje para enviar:");
							outputLine = stdIn.readLine();
							System.out.println("Cliente: " + outputLine);
							pOut.write(outputLine);
							estado++;
						} else {
							outputLine = "OK";
							System.out.println("Cliente (ERROR1 - El servidor no respondió acorde al protocolo): " + outputLine);
							pOut.write(outputLine);
							estado = 2;
							ejecutar = false;
						}
						break;
					case 1:
						try {
							int val = Integer.parseInt(inputLine);
							outputLine = "OK";
							System.out.println("Cliente: " + outputLine);
							pOut.write(outputLine);
							estado++;
						} catch (Exception e) {
							outputLine = "OK";
							System.out.println("Cliente (ERROR2 - El servidor no respondió acorde al protocolo): " + outputLine);
							pOut.write(outputLine);
							estado = 2;
							ejecutar = false;
						}
						break;
					default:
						outputLine = "ERROR";
						estado = 0;
						break;
				}
			}
			
		}
		
	}
}
