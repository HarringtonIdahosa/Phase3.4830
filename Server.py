import socket




# Set up UDP server socket
server_ip = '127.0.0.1'
server_port = 12345




server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))
print('UDP server up...')




# Receive file size from the client
file_size_packet, client_address = server_socket.recvfrom(1024)
file_size = int.from_bytes(file_size_packet[1:], 'big')
print("File size received:", file_size)




# Receive file data from the client
received_data = b""
expected_sequence_number = 0




while True:
  data_packet, client_address = server_socket.recvfrom(1024)




  sequence_number = data_packet[0]
  checksum = data_packet[1]
  data = data_packet[2:]




  # Verify checksum
  calculated_checksum = (sum(data) + sequence_number) & 0xFF




  # Verify sequence number
  if sequence_number != expected_sequence_number:
      print("Out of order packet. Packet discarded.")
      ack_packet = expected_sequence_number.to_bytes(1, 'big')
      server_socket.sendto(ack_packet, client_address)
      continue




  # Store the data and update sequence number
  received_data += data
  expected_sequence_number = (expected_sequence_number + 1) % 256




  # Send ACK
  ack_packet = sequence_number.to_bytes(1, 'big')
  server_socket.sendto(ack_packet, client_address)




  # Check for termination packet
  if len(data) < 1021:
      break




# Save the received data as a JPG file
file_name = 'received_image.jpg'
with open(file_name, 'wb') as file:
  file.write(received_data)




print("File received and saved as", file_name)




# Close the server socket
server_socket.close()

