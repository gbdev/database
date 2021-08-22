#ifndef STACK_H
#define STACK_H

typedef struct
{
    UINT8 values[256];
    UINT8 stSize;
} STACK;

void stackInit(STACK *st)
{
    UINT8 i;
    st->stSize = 0;
    for(i = 0; i < 256; i++)
        st->values[i] = 0;
}

UINT8 stackPush(STACK* st, UINT8 value)
{
    if(st->stSize == 255)
        return 0;
    st->values[st->stSize++] = value;
    return 1;
}

UINT8 stackPop(STACK *st)
{
    if(!st->stSize)
        return 255;
    return st->values[--(st->stSize)];
}

UINT16 stackTop(STACK *st)
{
	return(st->values[(st->stSize)-1]);
}
#endif
