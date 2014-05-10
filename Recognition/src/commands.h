/*
 * commands.h
 *
 *  Created on: Mar 20, 2013
 *      Author: James Mcclain, Antonis Kalou
 */

#ifndef COMMANDS_H_
#define COMMANDS_H_

#include "globals.h"

char *get_command(char *database,char *speech,int match_first,int starting_line,int *LINE_IN_DATABASE);
char *create_command(char *buf, int *LINE_IN_DATABASE);

#endif /* COMMANDS_H_ */
