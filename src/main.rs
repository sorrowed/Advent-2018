extern crate time;
extern crate regex;

mod day01;
mod day02;
mod day03;
mod day04;

fn main() {
    println!("01.1 Resulting frequency: {0}", day01::first());
    println!("01.2 First duplicate frequency: {0}", day01::second());
    println!("02.1 Checksum: {0}", day02::first());

    let start = time::precise_time_ns();
    let r = day02::second();
    let end = time::precise_time_ns();
    println!("02.2 {} {}", r, (end - start) / 1000);


	println!("03.1 Number of overlapping rectangles: {0}", day03::first());
    println!("03.2 None overlapping claim: {0}", day03::second());

	println!("04.1 <<>>: {0}", day04::first());
    println!("04.2 <<>>: {0}", day04::second());
}
