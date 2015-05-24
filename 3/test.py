# https://class.coursera.org/crypto-014/forum/thread?thread_id=143

rawhex1 = b'\x11'*1024
rawhex2 = b'\x22'*1024
rawhex3 = b'\x33'*1024
rawhex4 = b'\x44'*773
e1 = open('b1','wb')
e2 = open('b2','wb')
e3 = open('b3','wb')
e4 = open('b4','wb')
t1 = open('test11223344','wb')
e1.write(rawhex1)
e2.write(rawhex2)
e3.write(rawhex3)
e4.write(rawhex4)
t1.write(rawhex1+rawhex2+rawhex3+rawhex4)
t1.close()
e1.close()
e2.close()
e3.close()
e4.close()
