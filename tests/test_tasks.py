from fabric_remote.tasks import QueueIO
from Queue import Queue

def test_queueio_write():
    q = Queue()
    qio = QueueIO(q)
    qio.write('test')
    assert q.get() == {'output':'test'}

def test_queueio_random_methods():
    qio = QueueIO(Queue())
    assert qio.isatty() == False
    assert qio.flush() == None
