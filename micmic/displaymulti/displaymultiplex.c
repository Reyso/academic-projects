#define F_CPU 8000000UL
#include <avr/io.h>
#include <util/delay.h>
#include <avr/pgmspace.h> //biblioteca para gravar dados na memória flash
//vetor gravado na memória flash
const unsigned char Tabela[] PROGMEM ={0x40, 0x79, 0x24,0x30,0x19,0x12,
0x02, 0x78, 0x00, 0x18, 0x08, 0x03, 0x46,0x21,0x06,0x0E};


int main()
{unsigned char contador =0;	//Valor a ser exibido
	unsigned char digito =0;	//Digito a ser exibido
	unsigned char exibe =0;	//Quantidade de exibição
	signed char contagem = 1; //incremento do contador
	signed char estado = 1; //indica se a contagem crescente ou descrecente;
	DDRB = 0x03; //Configura PB0 e PB1 saida - 	0b0011
	PORTB = 0x07; //Desliga os dois displays e ativa o resistor de pull up (0111)
	DDRD = 0x7F; //PORTD como saída (display)
	PORTD = 0x7F; //Apaga todos os LEDs
	UCSR0B= 0x00; //PD0 e PD1 como I/O genérico
	
	while(1) //Laço infinito
	{digito= contador & 0x0F; //Digito menos significativo
		PORTD = pgm_read_byte(&Tabela[digito]);//Aciona PORTD
		PORTB = 0x02; //Exibe display 0
		_delay_ms(200); //Tempo display 0
		PORTB = 0x03; //Desliga os dois displays
		digito= (contador& 0xF0) >> 4; //Digito mais significativo
		PORTD = pgm_read_byte(&Tabela[digito]);//aciona PORTD
		PORTB = 0x01; //Exibe display 1
		_delay_ms(200); //Tempo display 1
		PORTB = 0x03; //Desliga os dois displays
		if (!(PINB & 0x04)) //se precionado = 0 falso e inverte para verdadeiro
		{	contagem = 0;
		} 
		else
		{ if (contagem==0) //botao estava pressionado? se sim...
			{ if (estado == 1) // crescente
			{
				contagem =-1; //contagem negativa
				estado =-1;
			}
			else
			{
				contagem =1; // se n contagem decrescente
				estado =1;
			}
			}
		}
		
		exibe+= contagem;  //incrementa contagem
		if (exibe==2) //incrementa contador apos n exibições
		{ contador+=contagem; exibe = 0; }
	}
}



/* //Display sem botao
int main()
{unsigned char contador =0;	//Valor a ser exibido
	unsigned char digito =0;	//Digito a ser exibido
	unsigned char exibe =0;	//Quantidade de exibição
	DDRB = 0x03; //Configura PB0 e PB1 saida - 	0b0011
	PORTB = 0x03; //Desliga os dois displays
	DDRD = 0x7F; //PORTD como saída (display)
	PORTD = 0x7F; //Apaga todos os LEDs
	UCSR0B= 0x00; //PD0 e PD1 como I/O genérico
	
	while(1) //Laço infinito
	{digito= contador & 0x0F; //Digito menos significativo
		PORTD = pgm_read_byte(&Tabela[digito]);//Aciona PORTD
		PORTB = 0x02; //Exibe display 0
		_delay_ms(30); //Tempo display 0
		PORTB = 0x03; //Desliga os dois displays
		digito= (contador& 0xF0) >> 4; //Digito mais significativo
		PORTD = pgm_read_byte(&Tabela[digito]);//aciona PORTD
		PORTB = 0x01; //Exibe display 1
		_delay_ms(30); //Tempo display 1
		PORTB = 0x03; //Desliga os dois displays
		exibe++; //incrementa exibe
		if (exibe==15) //incrementa contador apos n exibições
		{ contador++; exibe = 0; }
	}
}*/
