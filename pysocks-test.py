import socks

def is_tunnel_working(port=8080):
    s = socks.socksocket() # Same API as socket.socket in the standard lib
    try: 

        s.set_proxy(socks.SOCKS5, "localhost",port) # SOCKS4 and SOCKS5 use port 1080 by default
        s.settimeout(1.5)

        s.connect(("google.com", 80))

        request = """GET / HTTP/1.1
        Host: google.com
        User-Agent: MyClient/1.0

        """

        # convert to bytes for sending over network
        request_encoded = request.encode()

        s.sendall(request_encoded)

        # now receive the response
        buffer_size = 4096
        response = s.recv(buffer_size)

        s.close()
        return True
    except Exception as e:
        # print(e)
        return False

if __name__ == '__main__':
    print(is_tunnel_working())