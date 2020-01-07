#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <crypt.h>

bool checker(string originalhash, string newhash);

int main(int argc, string argv[])
{
    char key[] = {'\0', '\0', '\0', '\0', '\0', '\0'};
    if ((argc < 2 || argc > 2) && strlen(argv[1]) != 13)
    {
        printf("Usage: ./crack hash\n");
        return 1;
    }
    char salt[] = {argv[1][0], argv[1][1], '\0'};
    while (key[4] < 'z' + 1 && !checker(argv[1], crypt(key, salt)))
    {
        if (key[0] == '\0')
        {
            key[0] = 'A';
        }
        else if (key[0] == 'z' + 1)
        {
            key[0] = 'A';
            if (key[1] == '\0')
            {
                key[1] = 'A';
            }
            else if (key[1] == 'z')
            {
                if (key[2] == '\0')
                {
                    key[2] = 'A';
                }
                else if (key[2] == 'z')
                {
                    if (key[3] == '\0')
                    {
                        key[3] = 'A';
                    }
                    else if (key[3] == 'z')
                    {
                        if (key[4] == '\0')
                        {
                            key[4] = 'A';
                        }
                        else
                        {
                            key[4]++;
                        }
                        key[3] = 'A';
                    }
                    else
                    {
                        key[3]++;
                    }
                    key[2] = 'A';
                }
                else
                {
                    key[2]++;
                }
                key[1] = 'A';
            }
            else
            {
                key[1]++;
            }
        }
        else
        {
            key[0]++;
        }
    }
    printf("%s\n", key);
}


bool checker(string originalhash, string newhash)
{
    for (int i = 0, n = strlen(originalhash); i < n; i++)
    {
        if (originalhash[i] != newhash[i])
        {
            return false;
        }
    }
    return true;
}
