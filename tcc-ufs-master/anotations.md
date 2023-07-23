## ISO 25010
### ISO/IEC 25010
1. Estudar as normas de qualidade
2. https://iso25000.com/index.php/en/iso-25000-standards/iso-25010

## Radon
### Raw metrics
1. Número total de linhas de código
2. Número de linhas lógicas de código
3. Número de linhas de código fonte
4. Número de linhas com comentários
5. Número de linhas representando multi-line strings
6. Número de linhas em branco ou com apenas espaços em branco

### Cyclomatic complexity

####Cálculo de score:

| Construct         | Effect on CC | Reasoning                                                                               |
|-------------------|--------------|-----------------------------------------------------------------------------------------|
| if                | +1           | An if statement is a single decision.                                                   |
| elif	             | +1	          | The elif statement adds another decision.                                               |
| else	             | +0	          | The else statement does not cause a new decision. The decision is at the if.            |
| for	              | +1	          | There is a decision at the start of the loop.                                           |
| while	            | +1	          | There is a decision at the while statement.                                             |
| except	           | +1	          | Each except branch adds a new conditional path of execution.                            |
| finally	          | +0	          | The finally block is unconditionally executed.                                          |
| with	             | +1	          | The with statement roughly corresponds to a try/except block (see PEP 343 for details). |
| assert	           | +1	          | The assert statement internally roughly equals a conditional statement.                 |
| Comprehension	    | +1	          | A list/set/dict comprehension of generator expression is equivalent to a for loop.      |
| Boolean Operator	 | +1	          | Every boolean operator (and, or) adds a decision point.                                 |

####Cálculo de rank:

####rank=⌈score/10⌉−H(5−score)

Onde H(s) é a função step de Heaviside

