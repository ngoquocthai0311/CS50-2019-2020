#include "helpers.h"
#include <math.h>
#include <stdio.h>
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float average_color = round((float)(image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed)/3);
            image[i][j].rgbtBlue = image[i][j].rgbtGreen = image[i][j].rgbtRed = average_color;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        int temp_width = width - 1;
        for (int j = 0; j < round((float)(width/2)); j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][temp_width];
            image[i][temp_width] = temp;
            temp_width--;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE imageO[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            imageO[i][j] = image[i][j];
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float aver_red = 0;
            float aver_blue = 0;
            float aver_green = 0;
            int count = 0;
            for (int a = i - 1; a <= i + 1; a++)
            {
                for (int b = j - 1; b <= j + 1; b++)
                {
                    if (a < 0 || a > height - 1 || b < 0 || b > width - 1)
                    {
                        continue;
                    }
                    else
                    {
                        aver_red += imageO[a][b].rgbtRed;
                        aver_blue += imageO[a][b].rgbtBlue;
                        aver_green += imageO[a][b].rgbtGreen;
                        count++;
                    }
                }
            }
            aver_red = round((float)(aver_red / count));
            aver_blue = round((float)(aver_blue / count));
            aver_green = round((float)(aver_green / count));
            image[i][j].rgbtRed = aver_red;
            image[i][j].rgbtBlue = aver_blue;
            image[i][j].rgbtGreen = aver_green;
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE imageO[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            imageO[i][j] = image[i][j];
        }
    }
    float gx[9] = {-1, 0, 1, -2, 0, 2, -1, 0, 1};
    float gy[9] = {-1, -2, -1, 0, 0, 0, 1, 2, 1};
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float red_x = 0;
            float red_y = 0;
            float blue_x = 0;
            float blue_y = 0;
            float green_x = 0;
            float green_y = 0;
            int index = 0;
            for (int a = i - 1; a <= i + 1; a++)
            {
                for (int b = j - 1; b <= j + 1; b++)
                {
                    if (a < 0 || a >= height || b < 0 || b >= width)
                    {
                        ++index;
                        continue;
                    }
                    else
                    {
                        red_x += imageO[a][b].rgbtRed * gx[index];
                        red_y += imageO[a][b].rgbtRed * gy[index];

                        blue_x += imageO[a][b].rgbtBlue * gx[index];
                        blue_y += imageO[a][b].rgbtBlue * gy[index];

                        green_x += imageO[a][b].rgbtGreen * gx[index];
                        green_y += imageO[a][b].rgbtGreen * gy[index];
                        index++;
                    }
                }
            }
            float Red = round(sqrt(red_x * red_x + red_y * red_y));
            float Blue = round(sqrt(blue_x * blue_x + blue_y * blue_y));
            float Green = round(sqrt(green_x * green_x + green_y * green_y));
            image[i][j].rgbtRed = fmin(Red, 255);
            image[i][j].rgbtBlue = fmin(Blue, 255);
            image[i][j].rgbtGreen = fmin(Green, 255);
        }
    }
    return;
}
