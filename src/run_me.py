__author__ = 'soroosh'
from src.services import analysis_transaction

analysis_transaction('../inputs/sample_input.csv', '../outputs/sample_output.csv')
analysis_transaction('../inputs/sample_input.json', '../outputs/sample_output.json')
analysis_transaction('../inputs/sample_input.txt', '../outputs/sample_output.txt')
analysis_transaction('../inputs/sample_input.xml', '../outputs/sample_output.xml')


