import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/

class TrafficLight {
    private int distance;
    private int duration;

    TrafficLight(int distance, int duration) {
        this.distance = distance;
        this.duration = duration;
    }

    private boolean isGreen(double time) {
        int nbSwitch = (int) Math.floor(time / this.duration);

        // System.err.println("nb switch " + nbSwitch);

        if ((nbSwitch % 2) == 0) {
            // System.err.println(time % this.duration);
            // if (time % this.duration < 1 & time % this.duration > 0) {
            //     return false;
            // }

            return true;
        } else {

            return false;
        }
    }

    private double timeToReach(int speed) {
        double speedMeterPerSecond = (double) speed / 3.6;
        return (double) this.distance / speedMeterPerSecond;
    }

    boolean greenWhenReaching(int speed) {
        if (speed==60 & !this.isGreen(this.timeToReach(speed))) {
            System.err.println("duration s " + this.duration);
            System.err.println("distance m " + this.distance);
            System.err.println("speed k/h " + speed);
            System.err.println("speed m/s " + speed / 3.6);
            System.err.println("timeToReach " + this.timeToReach(speed));
            System.err.println("is grren computation " + ((this.timeToReach(speed) / this.duration) % 2));
        }
        return this.isGreen(this.timeToReach(speed));
    }
}

class Solution {

    public static void main(String args[]) {
        Scanner in = new Scanner(System.in);
        int speed = in.nextInt();
        int lightCount = in.nextInt();
        List<TrafficLight> trafficLights = new ArrayList<TrafficLight>();
        for (int i = 0; i < lightCount; i++) {
            int distance = in.nextInt();
            int duration = in.nextInt();
            trafficLights.add(new TrafficLight(distance, duration));
        }

        while (true) {
            System.err.println("");

            boolean redLight = false;
            for (TrafficLight light: trafficLights) {
                if (!light.greenWhenReaching(speed)) {
                    redLight = true;
                    break;
                }
            }
            if (redLight) {
                speed --;
            } else {
                break;
            }
        }

        // Write an action using System.out.println()
        // To debug: System.err.println("Debug messages...");
        System.out.println(speed);
    }
}