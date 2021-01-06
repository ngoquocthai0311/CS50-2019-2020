#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
// define the value of one byte.
int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        return 1;
    }

    // declare needed values
    char imgname[8];
    unsigned char buffer[512];
    FILE *img = NULL;
    int count = 0;
    bool isJpgHeader = false;
    while (fread(buffer, 512, 1, file) == 1)
    {
        //int elementsRead = fread(buffet, sizeof(BYTE), 512, file);
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If we have found the head of JPEG file
            if (isJpgHeader)
            {
                // stop the writing process
                fclose(img);
            }
            else // if we have not found any first JPEG file
            {
                isJpgHeader = true;
            }
            // creat a new JPEG file
            sprintf(imgname, "%03d.jpg", count++);
            img = fopen(imgname, "w");
        }
        // If we have found the JPEG file and the buffer does not valid for header of a JPEG file
        if (isJpgHeader)
        {
            fwrite(&buffer, 512, 1, img);
        }

    }
    // close files
    fclose(file);
    fclose(img);

    return 0;
}
