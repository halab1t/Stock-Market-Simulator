use plotters::prelude::*;
use rand::prelude::*;
use rand_distr::Normal;

fn simulate_brownian_path(start_price: f64, mu: f64, sigma: f64, time_steps: usize, delta_t: f64) -> Vec<f64> {
    let mut rng = thread_rng();
    let normal = Normal::new(0.0, 1.0).unwrap();
    let mut path = vec![start_price];
    let mut current_price = start_price;

    for _ in 1..time_steps {
        let z = normal.sample(&mut rng);
        let delta_w = z * delta_t.sqrt();
        let drift = (mu - 0.5 * sigma.powi(2)) * delta_t;
        let diffusion = sigma * delta_w;
        current_price *= (drift + diffusion).exp();
        path.push(current_price);
    }

    path
}

fn plot_live(prices: &[f64], time_step: usize) -> Result<(), Box<dyn std::error::Error>> {
    let root = BitMapBackend::new("plot.png", (640, 480)).into_drawing_area();
    root.fill(&WHITE)?;

    let mut chart = ChartBuilder::on(&root)
        .caption("Stock Price Path", ("sans-serif", 20).into_font())
        .margin(5)
        .x_label_area_size(40)
        .y_label_area_size(60)
        .build_cartesian_2d(0.0..(time_step as f64), prices.iter().cloned().collect::<Vec<f64>>().into_iter().min_by(|a, b| a.partial_cmp(b).unwrap()).unwrap()..prices.iter().cloned().collect::<Vec<f64>>().into_iter().max_by(|a, b| a.partial_cmp(b).unwrap()).unwrap())?;

    chart.configure_mesh()
        .x_desc("Time Steps")
        .y_desc("Price")
        .draw()?;

    chart
        .draw_series(LineSeries::new(
            (0..time_step).map(|i| (i as f64, prices[i])),
            &RED,
        ))?
        .label("Price Path")
        .legend(|(x, y)| PathElement::new(vec![(x, y), (x + 20, y)], &RED));

    chart.configure_series_labels()
        .background_style(&WHITE.mix(0.8))
        .border_style(&BLACK)
        .draw()?;

    root.present()?;
    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let start_price: f64 = 100.0;
    let mu: f64 = 0.05; // Annual drift (5%)
    let sigma: f64 = 0.2; // Annual volatility (20%)
    let delta_t: f64 = 1.0 / 252.0; // Daily steps (252 trading days)
    let time_steps = 252;

    let mut prices = vec![start_price];
    let mut rng = thread_rng();
    let normal = Normal::new(0.0, 1.0).unwrap();
    let mut current_price = start_price;

    // Live plotting loop
    for step in 1..time_steps {
        let z = normal.sample(&mut rng);
        let delta_w = z * delta_t.sqrt();
        let drift = (mu - 0.5 * sigma.powi(2)) * delta_t;
        let diffusion = sigma * delta_w;
        current_price *= (drift + diffusion).exp();
        prices.push(current_price);

        // Plot every few steps for smoothness
        if step % 10 == 0 || step == time_steps - 1 {
            plot_live(&prices, prices.len())?;
            std::thread::sleep(std::time::Duration::from_millis(100)); // Slow down to see updates
        }
    }

    println!("Simulation complete. Check plot.png for the final path.");
    Ok(())
}
