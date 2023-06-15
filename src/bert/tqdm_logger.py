import logging
import time
from tqdm import tqdm
import io

class TqdmToStdout(io.StringIO):
    """
        Output stream for TQDM which will output to StdOut.
    """
    logger = None
    level = None
    buf = ''
    def __init__(self,logger,level=None):
        super(TqdmToStdout, self).__init__()
        self.logger = logger
        self.level = level or logging.INFO
    def write(self,buf):
        self.buf = buf.strip('\r\n\t ')
        print(self.buf, file=sys.stdout)
    def flush(self):
        self.logger.log(self.level, self.buf)