# py module

######################################################################
#
# Dropshare
#

class Dropshare(object):
    def __init__(self):
        pass
    def getMethod(self):
        return None

class LocalDropshare(Dropshare):
    """I use this during testing, and when I made a 'dropshare' available via an arbitrary fusefs mount :-)"""
    def __init__(self, basepath):
        super().__init__(self)
        self.basepath = basepath
    def getMethod(self):
        return "local"

class FtpDropshare(Dropshare):
    def __init__(self, host, path, username, password):
        super().__init__(self)
        self.username = username
        self.password = password
        self.host = host
        self.path = path
    def getMethod(self):
        return "ftp"

class WebdavDropshare(Dropshare):
    def __init__(self, baseurl, username, password):
        super().__init__(self)
        self.username = username
        self.password = password
        self.baseurl = baseurl
    def getMethod(self):
        return "webdav"


######################################################################
#
# Message box
#

class MessageBox(object):
    def __init__(self):
        pass
    def getMethod(self):
        return None
    def getUri(self):
        return None

class Pop3MessageBox(MessageBox):
    def __init__(self, host, username, password, port=None):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
    def getMethod(self):
        return "pop3"
    def getUri(self):
/ssl.html#        """pop3://[UserName@]Host[:Port][?Options]
        @see http://fusesource.com/docs/router/1.5/component_ref/POPComp.html
        """
        res = [ "pop3://", self.username, "@", self.host ]
        if self.port:
            res.append(":%s" % self.port)
        res.append("?password=%s" % self.password)
        return "".join(res)

class RedisMessageBox(MessageBox):
    """Where I pickup messages to me"""
    def __init__(self, host, hostFromOutside, port=None, key="dropy:box", auth=None):
        self.host = host
        self.hostFromOutside = hostFromOutside
        self.port = port
        self.key = key
        assert self.auth is None or "*" not in self.auth, "auth '%s' must not contain an *" % self.auth
        self.auth = auth # 'AUTH password' required?
    def getMethod(self):
        return "redis"
    def getUri(self):
        """redis://host:port/auth*key"""
        res = [ "redis://" ]
        res.append(self.hostFromOutside)
        if self.port: res.append(":%s" % self.port)
        res.append("/")
        if self.auth: res.append("%s*" % self.auth)
        res.append("%s" % self.key)
        return "".join(res)



######################################################################
#
# Yourself
#


class Yourself(object):
    """represends the user that sits in front of this computer, who owns the local files"""

    def __init__(self):
        self.cryptkey = None
        self.dropshares = LocalDropshare('/tmp/drop')
        self.messagebox = []
