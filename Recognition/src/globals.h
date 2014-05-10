/*
 * globals.h
 *
 *  Created on: Mar 20, 2013
 *      Author: James Mcclain, Antonis Kalou
 */

#ifndef GLOBALS_H_INCLUDED
#define GLOBALS_H_INCLUDED

struct variables{
  char *varName;
  char *varValue;

  struct variables *next;
};

struct config {
  int match_first, starting_db_line, current_db_line, store_variables;
  struct variables *var_Header, *var_LL;
};

#endif /* GLOBALS_H_INCLUDED */
