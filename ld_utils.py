import string

def url_formatter(url):
    if (string.find(url, 'http://') == 0):
        url = url[7:len(url)]
    return url

#TODO: excepciones
def get_host_port_route(url):
    url = url_formatter(url)
    url_tokens = string.split(url, '/')
    route = ''
    for i in range(1,len(url_tokens)):
        if url_tokens[i] != '':
            route = route + '/' + url_tokens[i]
    host_tokens = string.split(url_tokens[0], ':')
    host = host_tokens[0]
    if (len(host_tokens) <= 1):
        port = 80
    elif(len(host_tokens) == 2):
        port = int(host_tokens[1])
    return host, port, route

def LongestCommonSubstring(S1, S2):
    M = [[0]*(1+len(S2)) for i in xrange(1+len(S1))]
    longest, x_longest = 0, 0
    for x in xrange(1,1+len(S1)):
        for y in xrange(1,1+len(S2)):
            if S1[x-1] == S2[y-1]:
                M[x][y] = M[x-1][y-1] + 1
                if M[x][y]>longest:
                    longest = M[x][y]
                    x_longest  = x
            else:
                M[x][y] = 0
    return S1[x_longest-longest: x_longest]
