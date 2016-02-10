import unittest 
from unittest import TestResult 
from pexpect import spawn
import sys

class TestExemplo1(unittest.TestCase): 

    file = ''

    def setUp(self):
        ###########################################
        # Nao altere esse trecho (Inicio)
        ###########################################
        self.file = str(sys.argv[1]) + str(sys.argv[2])
        ###########################################
        # Nao altere esse trecho (Final)
        ###########################################
        # insira inicializacoes dos testes apos esse comentario


    def tearDown(self):
        pass


# metodos de teste devem ser inseridos aqui
    def test_soma1(self):
        child = spawn('python ' + self.file)
        child.sendline('30')
        child.sendline('10')
        child.sendline('2')
        child.expect('42')
        

if __name__== '__main__':
    ###########################################
    # Nao altere esse trecho (Inicio)
    ###########################################
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestExemplo1)
    r = TestResult()
    suite.run(r)

    result_file = open(str(sys.argv[1]) + '/submissao/' + str(sys.argv[3] + 'result.txt', 'wb'))
    result_file.write(str(len(r.errors)))
    result_file.write('\n')
    result_file.write(str(len(r.failures)))
    result_file.write('\n')
    result_file.write(str(r.testsRun))
    result_file.write('\n')
    result_file.write(str(r.wasSuccessful()))
    result_file.write('\n')
    result_file.close()
    ###########################################
    # Nao altere esse trecho (Final)
    ###########################################
