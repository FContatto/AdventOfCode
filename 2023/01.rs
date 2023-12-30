use std::fs::File;
use std::io::{BufReader,BufRead};

static NUMBERS_MAP: [(&str, char); 9] = [("one", '1'),("two", '2'),("three", '3'),("four", '4'),("five", '5'),
("six", '6'),("seven", '7'),("eight", '8'),("nine", '9')];

fn get_number(input_s: String, question_2: bool)->u32{
    let mut first_digit = 0;
    let mut first_digit_found = false;
    let mut second_digit = 0;
    for (i,c) in input_s.chars().enumerate(){
        let mut digit_char = c;
        if question_2{
            if !digit_char.is_digit(10){
                for (k,v) in NUMBERS_MAP.iter(){
                    if i+k.len() <= input_s.len(){
                        if **k==input_s[i..(i+k.len())]{
                            digit_char = *v;
                            break;
                        }
                    }
                }
            }
        }
        if digit_char.is_digit(10){
            if first_digit_found{
                second_digit = digit_char.to_digit(10).unwrap();
            }
            else{
                first_digit_found = true;
                first_digit = digit_char.to_digit(10).unwrap();
                second_digit = first_digit;
            }
        }
    }
    let number = first_digit*10+second_digit;
    number
}


fn main() {
    let file = File::open("src\\input.txt").expect("Failed to read file.");
    let solve_question_2 = true;
    let mut sum = 0;
    let reader = BufReader::new(file);
    for s in reader.lines(){
        sum += get_number(s.unwrap(), solve_question_2);
    }
    println!("{}", sum);
}
