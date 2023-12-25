import socket


# Set up UDP client socket
server_ip = '127.0.0.1'
server_port = 12345


client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# Read the JPG file to be sent
file_name = 'image.jpg'
with open(file_name, 'rb') as file:
   file_data = file.read()


# Send file size to the server
file_size = len(file_data)
file_size_packet = file_size.to_bytes(4, 'big')
client_socket.sendto(file_size_packet, (server_ip, server_port))
print("File size sent:", file_size)


# Send file data to the server
packet_size = 1022
total_packets = (file_size) // packet_size + 1
for i in range(total_packets):
   start_idx = i * packet_size
   end_idx = start_idx + packet_size
   data_packet = bytearray()
   data_packet.append(i % 256)  # Sequence number
   data_packet.append(0)  # Placeholder for checksum
   data_packet.extend(file_data[start_idx:end_idx])
   checksum = sum(data_packet) & 0xFF
   data_packet[1] = 0xFF - checksum  # Set checksum as 1's complement
   client_socket.sendto(data_packet, (server_ip, server_port))
   print("Packet sent, sequence number#:", i)


   # Receive ACK from the server
   ack_packet, server_address = client_socket.recvfrom(1024)
   if ack_packet != ack_packet:
       print("ACK not received. Error in transmission.")
       break


print("File sent")


# Close the client socket
client_socket.close()
