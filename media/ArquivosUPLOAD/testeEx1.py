# -*- coding: utf-8 -*-
from pexpect import spawn
import sys
import sqlite3
import unittest 
from unittest import TestResult

class TestExemplo1(unittest.TestCase): 

    submissao_id = 0
    file = ''

    def setUp(self):
        ###########################################
        # Nao altere esse trecho (Inicio)
        ###########################################
        self.file = str(sys.argv[1]) + '/' + str(sys.argv[2])
        self.submissao_id = str(sys.argv[4])
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

    def test_soma2(self):
        child = spawn('python ' + self.file)
        child.sendline('-30')
        child.sendline('-10')
        child.sendline('-2')
        child.expect('-42')

if __name__== '__main__':
    ###########################################
    # Nao altere esse trecho (Inicio)
    ###########################################
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestExemplo1)
    r = TestResult()
    suite.run(r)

    # sqlite
    # Connecting to the database file
    conn = sqlite3.connect('/home/alexandre/git/safira/safira.sqlite3')
    c = conn.cursor()
    
    
    
    c.execute("UPDATE programacao_alunosubmissaoexerciciopratico SET avaliacao=90 WHERE id=1")
    # Committing changes and closing the connection to the database file
    conn.commit()
    conn.close()

#     result_file = open(str(sys.argv[1]) + '/teste/' + str(sys.argv[3]) + '/result.txt', 'wb')
#     result_file.write(str(len(r.errors)))
#     result_file.write('\n')
#     result_file.write(str(len(r.failures)))
#     result_file.write('\n')
#     result_file.write(str(r.testsRun))
#     result_file.write('\n')
#     result_file.write(str(r.wasSuccessful()))
#     result_file.write('\n')
#     result_file.close()

    ###########################################
    # Nao altere esse trecho (Final)
    ###########################################
