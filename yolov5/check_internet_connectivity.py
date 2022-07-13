import socket
REMOTE_SERVER = "www.google.com"
def is_connected(hostname):
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(hostname)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    s.close()
    return True
  except:
    return False


if __name__ == "__main__":
  while(True):
    print("connected: %s" % is_connected(REMOTE_SERVER))
