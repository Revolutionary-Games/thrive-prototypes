//way too much including, lol

#include <iostream>
#include <math.h>
#include <cmath>
#include <stdlib.h>
#include <time.h>
#include <algorithm>

class organelle{
public:
    char letter;
    int size_x;
    int size_y;
};

class placed_organelle{
public:
    organelle organelle;
    int pos_q;
    int pos_r;
};

//this is a point in the grid which can have a letter in it
class point{
public:
    int pos_x;
    int pos_y;
    float pos_cart_x;
    float pos_cart_y;
    float distance;
    bool available;
};

/* convert from axial to cartesian
this is good because it means the cells will be ~circular when on the hex grid*/
float axialtocartesianx(int q, int r, float HEX_SIZE){
    return q * HEX_SIZE * 3 / 2;
}

float axialtocartesiany(int q, int r, float HEX_SIZE){
    return HEX_SIZE * sqrt(3) * (r + q / 2);
}

/*find the distance between 2 points */

float distance(float x, float y, float x2, float y2) {
    return sqrt(pow((x - x2),2) + pow((y - y2),2));
}


/*display the grid */

void printArray(char (&grid)[50][50])
{
    for(int x = 0; x < 50; x++){
        for(int y = 0; y < 50; y++){
            std::cout << grid[x][y] << " ";
        }
        std::cout << "\n";
    }
}

/*check if a space is free */

bool checkspace(int x, int y, organelle org, char (&grid)[50][50])
{
    bool answer = true;
    for(int i = x; i < x + org.size_x; i++){
        for(int j = y; j < y + org.size_y; j++){
            if (grid[i][j] != '.')
                answer = false;
        }
    }
    return answer;
}

//add an organelle to the grid by putting letters down

void add_organelle(int x, int y, organelle org, char (&grid)[50][50]){
    for (int i = x; i < x + org.size_x; i++){
        for (int j = y; j < y + org.size_y; j++){
            grid[i][j] = org.letter;
        }
    }
}
//used for sorting the points by distance from the center

bool operator<(point const & a, point const & b)
{
    return a.distance < b.distance;
}

//find a space to put the current organelle, search by closest point to nucleus, inefficient

void find_space(char (&grid)[50][50], organelle org, point (&points)[2500], int& counter, int counter_base, int& x, int& y)
{
    counter = counter_base;
    int check_x;
    int check_y;
    bool found = false;
    while (found == false){
        check_x = points[counter].pos_x;
        check_y = points[counter].pos_y;
        if (checkspace(check_x, check_y, org, grid)){
            x = check_x;
            y = check_y;
            found = true;
        }
        counter++;
        if (counter == 2500){
            std::cout << "ERROR : CANT FIND A SPACE FOR AN ORGANELLE!!!";
            found = true;
        }
    }
}

int main() {

    float HEX_SIZE = 2; //size of the hexes in the game, not really important

    /*list of possible organelles */
    organelle nucleus;
    nucleus.letter = 'n';
    nucleus.size_x = 2;
    nucleus.size_y = 2;

    organelle cytoplasm;
    cytoplasm.letter = 'c';
    cytoplasm.size_x = 1;
    cytoplasm.size_y = 1;

    organelle mitochondria;
    mitochondria.letter = 'm';
    mitochondria.size_x = 1;
    mitochondria.size_y = 2;

    organelle vacuole;
    vacuole.letter = 'v';
    vacuole.size_x = 2;
    vacuole.size_y = 2;

    organelle chloroplast;
    chloroplast.letter = 'h';
    chloroplast.size_x = 1;
    chloroplast.size_y = 2;

    organelle toxin;
    toxin.letter = 't';
    toxin.size_x = 1;
    toxin.size_y = 1;

    organelle flagella;
    flagella.letter = 'f';
    flagella.size_x = 1;
    flagella.size_y = 1;

    /* make a random list of organelles to add
    This should be replaced with reading the codes from a file*/
    int number_of_organelles_interior = 10;
    int number_of_organelles_exterior = 5;
    int total_organelles = number_of_organelles_exterior + number_of_organelles_interior;
    int max_number_of_organelles = 20;
    if (total_organelles >= max_number_of_organelles){
        std::cout << "ERROR : TOO MANY ORGANELLES.";
    }

    srand ( time(NULL) );
    char letters[4] = {'m', 'c', 'h', 'v'};
    char organelles[max_number_of_organelles];
    organelles[0] = 'n'; //always have only 1 nucleus
    organelles[1] = 'c'; //always have at least 1 cytoplasm
    for (int i = 2; i < number_of_organelles_interior; i++){
        int RandIndex = rand() % 4;
        organelles[i] = letters[RandIndex];
    }
    char letters_ext[2] = {'f', 't'};
    for (int i = number_of_organelles_interior; i < total_organelles; i++){
        int RandIndex = rand() % 2;
        organelles[i] = letters_ext[RandIndex];
    }

    std::cout << "List of Organelles to make : ";
    for (int i = 0; i < total_organelles; i++){
        std::cout << organelles[i];
    }
    std::cout << "\n";

    /* make a grid in axial coordinates and initialise to empty*/
    char grid[50][50];
    for(int x = 0; x < 50; x++){
        for(int y = 0; y < 50; y++){
            grid[x][y] = '.';
        }
    }

    /* make a list of all possible available spaces
    and sort this list by real distance in the hex space*/
    point points[2500];
    for (int i = 0; i < 50; i++){
        for (int j = 0; j < 50; j++){
            points[50*i + j].pos_x = i;
            points[50*i + j].pos_y = j;
            points[50*i + j].pos_cart_x = axialtocartesianx(i,j,HEX_SIZE);
            points[50*i + j].pos_cart_y = axialtocartesiany(i,j,HEX_SIZE);
            points[50*i + j].distance = distance(points[50*i + j].pos_cart_x,
                                                 points[50*i + j].pos_cart_y,
                                                 axialtocartesianx(25,25,HEX_SIZE),
                                                 axialtocartesiany(25,25,HEX_SIZE));
        }
    }

    std::sort(points, points + 2500);

    /* place the organelles on the interior (nuclues / mitochondria / cytoplasm etc) */
    placed_organelle placed_organelles[total_organelles];

    int counter = 0; //keep track of what position you are in the list of available points
    int counter_base = 0; //used when putting exterior organelles outside interior ones
    int found_pos_x = 0;
    int found_pos_y = 0;
    bool placing_interior = true;
    int letter_position = 0;
    //so much copy and past #shame
    while (placing_interior){
        if (organelles[letter_position] == 'n'){
            find_space(grid, nucleus, points, counter, counter_base, found_pos_x, found_pos_y);
            add_organelle(found_pos_x, found_pos_y, nucleus, grid);
            placed_organelles[letter_position].organelle = nucleus;
        }
        if (organelles[letter_position] == 'c'){
            find_space(grid, cytoplasm, points, counter, counter_base, found_pos_x, found_pos_y);
            add_organelle(found_pos_x, found_pos_y, cytoplasm, grid);
            placed_organelles[letter_position].organelle = cytoplasm;
        }
        if (organelles[letter_position] == 'm'){
            find_space(grid, mitochondria, points, counter, counter_base, found_pos_x, found_pos_y);
            add_organelle(found_pos_x, found_pos_y, mitochondria, grid);
            placed_organelles[letter_position].organelle = mitochondria;
        }
        if (organelles[letter_position] == 'h'){
            find_space(grid, chloroplast, points, counter, counter_base, found_pos_x, found_pos_y);
            add_organelle(found_pos_x, found_pos_y, chloroplast, grid);
            placed_organelles[letter_position].organelle = chloroplast;
        }
        if (organelles[letter_position] == 'v'){
            find_space(grid, vacuole, points, counter, counter_base, found_pos_x, found_pos_y);
            add_organelle(found_pos_x, found_pos_y, vacuole, grid);
            placed_organelles[letter_position].organelle = vacuole;
        }
        placed_organelles[letter_position].pos_q = found_pos_x;
        placed_organelles[letter_position].pos_r = found_pos_y;
        letter_position++;
        if (organelles[letter_position] == 'f' || organelles[letter_position] == 't')
            placing_interior = false;
        }

    /*place the organelles on the exterior (flagella / agents / pilli) */
    int gap_between_int_and_ext = 10; //leave 10 free spaces so that exterior organelles are always on the outside
    counter_base = counter + gap_between_int_and_ext; //set a new start position for testing
    for (int i = letter_position; i < total_organelles; i++){
        if (organelles[letter_position] == 'f'){
            find_space(grid, flagella, points, counter, counter_base, found_pos_x, found_pos_y);
            add_organelle(found_pos_x, found_pos_y, flagella, grid);
            placed_organelles[letter_position].organelle = flagella;
        }
        if (organelles[letter_position] == 't'){
            find_space(grid, toxin, points, counter, counter_base, found_pos_x, found_pos_y);
            add_organelle(found_pos_x, found_pos_y, toxin, grid);
            placed_organelles[letter_position].organelle = toxin;
        }
        placed_organelles[letter_position].pos_q = found_pos_x;
        placed_organelles[letter_position].pos_r = found_pos_y;
        letter_position++;
    }
    /* show the result */
    printArray(grid);
    for (int i = 0; i < total_organelles; i++){
        std::cout << placed_organelles[i].pos_q << ",";
        std::cout << placed_organelles[i].pos_r << ",";
        std::cout << placed_organelles[i].organelle.letter << "\n";
    }


}
