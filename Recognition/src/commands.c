/*
 * commands.c
 *
 *  Created on: Mar 20, 2013
 *      Author: James Mcclain, Antonis Kalou
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <error.h>
#include <assert.h>
#include "commands.h"

// PROTOTYPES *****************

void store_special_variables(char *speech,char *buf);

//****************************

/**
* Return the command corresponding to /speech/ according to the dictionary file named /database/
*/
char *get_command(char *database,char *speech,int match_first,int starting_line,int *LINE_IN_DATABASE) {

  FILE *file;
  char buf[1024];
  char *ret = NULL; // The command to return.

  file = fopen(database,"r");
  if(file == NULL) {
    perror("fopen");
    exit(EXIT_FAILURE);
  }

  int i;
  if(starting_line != 0) {
    for(i = 0;i < starting_line;++i) {
      if(!(fgets(buf,1024,file))) {
      	goto success;
      }
    }
    ++*LINE_IN_DATABASE;
  }

  while( fgets(buf,1024,file)) {
    ++*LINE_IN_DATABASE;
    if(is_match(speech,buf)) {
      // Yes the speech matches, now to get variables in it.
      STORE_VARIABLES = 1;
      store_special_variables(speech,buf);
      is_match(speech,buf); // Will now store variables in in a LL

      char *got = fgets(buf,1024,file);
      if (got == NULL) {
        printf("Error in database, waiting command but got EOF.\n");
        exit(1);
      }
      ++*LINE_IN_DATABASE;
      ret = create_command(buf, LINE_IN_DATABASE);
      break;
    }
  }
  
 success:
  fclose(file);
  return ret;
}

/**
* Create the command, using the given line of dictionary /buf/ and the variables stored in /var_LL/
*/
char *create_command(char *buf, int *LINE_IN_DATABASE) {

  /* while(var_Header != NULL) { */
  /*   printf("%s == %s\n",var_Header->varName,var_Header->varValue); */
  /*   var_Header = var_Header->next; */

  /* } */
  /* printf("%s\n",buf); */
  char *ret = malloc(sizeof(char)*1024); // get a kilo at a time
  if(ret == NULL) {
  perror("malloc:");
  exit(EXIT_FAILURE);
  }
  int i = 0;
  char saveChar;
  char *startVarName;
  char *tmpCharPtr;
  struct variables *tmpHeader;

  // First skip leading spaces
  if(*buf != ' ' && *buf != '\t') {
    fprintf(stderr,"Bad syntax in database command: line %i does not start with a space\n", *LINE_IN_DATABASE);
    exit(EXIT_FAILURE);
  }
  while(*buf == ' ' || *buf == '\t') {
    ++buf;
  }
  while(*buf != '\0' && *buf != '\n' && *buf != '\r' && *buf != '#') {

    if( i % 1023) {
      ret = realloc(ret,sizeof(char)*1024*((i/1023)+1));
      if(ret == NULL) {
      	perror("malloc:");
      	exit(EXIT_FAILURE);
      }
    }
    if(*buf == '\\') {
      buf++;
      if(*buf == '\n' || *buf == '\0' || *buf == '\r') {
        fprintf(stderr,"Bad syntax in database command: '\\' char at the end, line %i\n", *LINE_IN_DATABASE);
      	exit(EXIT_FAILURE);
      }
      ret[i] = *buf;
    }
    else if(*buf != '$') {
      ret[i] = *buf;
    } else {
      ++buf;
      if(*buf == '$') {
      	printf("Bad syntax in database command: unexpected '$', line %i\n", *LINE_IN_DATABASE);
      	exit(EXIT_FAILURE);
      }
      if(*buf == '\n' || *buf == '\0' || *buf == '\r') {
      	printf("Bad syntax in database command: unexpected EOL, line %i\n", *LINE_IN_DATABASE);
      	exit(EXIT_FAILURE);
      }
      startVarName = buf;
      while(*buf != '$' && *buf != '\n' && *buf != '\0' && *buf != '\r') {
      	++buf;
      }

      if(*buf != '$') {
        fprintf(stderr,"Bad syntax in database command: lacking '$', line %i\n", *LINE_IN_DATABASE);
      	exit(EXIT_FAILURE);
      }

      saveChar = *buf;
      *buf = '\0';
      tmpHeader = var_Header;

      while(tmpHeader != NULL) {
      	if(strcmp(startVarName,tmpHeader->varName) == 0) {

      	  tmpCharPtr = tmpHeader->varValue;

      	  while(*tmpCharPtr != '\0') {

      	    ret[i] = *tmpCharPtr;
      	    ++i;
      	    ++tmpCharPtr;

      	    // It technically could happen.
      	    if( i % 1023) {
      	      ret = realloc(ret,sizeof(char)*1024*((i/1023)+1));
      	      if(ret == NULL) {
            		perror("malloc:");
            		exit(EXIT_FAILURE);
      	      }
      	    }

      	  }
          --i;
          *buf = saveChar;
      	}
      	// We found a match so leave this loop.
        if(*buf != '\0') {
          break;
      	}
      	tmpHeader = tmpHeader->next;
      }
      if(tmpHeader == NULL) {
      	--i;
      	*buf = saveChar;
      }

    }
     ++i;
    ++buf;
  }
  ret[i] = '\0';

  return ret;
}

/**
* Create the var_LL linked list, then set up the special variable SPEECH 
*/
void store_special_variables(char *speech,char *buf) {
  assert(var_LL == NULL);
  
  // first time add special var $SPEECH$
  var_LL = malloc(1*sizeof(struct variables));
  if(var_LL == NULL) {
    perror("malloc:");
    exit(EXIT_FAILURE);
  }
  // Set the var_Header to access the head later.
  var_Header = var_LL;
  var_LL->next = NULL;
  // The stupid error before "var_LL->next == NULL;"
  var_LL->varName = malloc(strlen("SPEECH")+1);
  strcpy(var_LL->varName,"SPEECH");
  var_LL->varValue = malloc(strlen(speech)+1);
  strcpy(var_LL->varValue,speech);
}
