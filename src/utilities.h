/*
 * utilities.h
 *
 *  Created on: 5 Mar 2020
 *      Author: hinchr
 */

#ifndef UTILITIES_H_
#define UTILITIES_H_

/************************************************************************/
/******************************  Macros     *****************************/
/************************************************************************/

#define max(x,y) ((x) > (y) ? (x) : (y))
#define min(x,y) ((x) < (y) ? (x) : (y))
#define ifelse(x,y,z) ((x) ? (y) : (z))
#define round_random( x ) ( (long int) ( floor( x ) + gsl_ran_bernoulli( rng, x - floor(x) ) ) )
#define ring_inc( x, n ) ( ( x ) = ifelse( ( x ) == ( ( n ) -1 ), 0 , ( x ) + 1 ) );

/************************************************************************/
/******************************  Functions  *****************************/
/************************************************************************/

void print_exit( char* );
void gamma_draw_list( int*, int, double, double );

#endif /* UTILITIES_H_ */
