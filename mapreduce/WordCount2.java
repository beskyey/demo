package test.mr;

import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

public class WordCount2 extends Configured implements Tool {

	//Mapper Class
	public static class WCMapper extends
			Mapper<LongWritable, Text, Text, IntWritable> {
 
		private Text mapOutputKey = new Text();
		private IntWritable mapOutputValue = new IntWritable(1);

		@Override
		public void map(LongWritable key, Text value, Context context)
				throws IOException, InterruptedException {

			// get line value
			String lineValue = value.toString();

			// split
			String[] strs = lineValue.split(" ");

			// iterator
			for (String str : strs) {
				// set map output key
				mapOutputKey.set(str);

				// output
				context.write(mapOutputKey, mapOutputValue);
			}
		}
	}

	//Reduce Class
	public static class WCReducer extends
			Reducer<Text, IntWritable, Text, IntWritable> {

		private IntWritable outputValue = new IntWritable();

		@Override
		protected void reduce(Text key, Iterable<IntWritable> values,
				Context context) throws IOException, InterruptedException {

			// temp: sum
			int sum = 0;

			// iterator
			for (IntWritable value : values) {
				sum += value.get();
			}
			// set output value
			outputValue.set(sum);

			// output
			context.write(key, outputValue);
		}

	}
	//Driver
	public int run(String[] args) throws Exception {

		Configuration configuration = this.getConf();
		Job job = Job.getInstance(configuration, this.getClass().getSimpleName());
		job.setJarByClass(this.getClass());

		// set job
		// input
		Path inpath = new Path(args[0]);
		FileInputFormat.addInputPath(job, inpath);

		// output
		Path outpath = new Path(args[1]);
		FileOutputFormat.setOutputPath(job, outpath);

		// mapper
		job.setMapperClass(WCMapper.class);
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(IntWritable.class);

		// reducer
		job.setReducerClass(WCReducer.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(IntWritable.class);

		// submit job
		boolean isSuccess = job.waitForCompletion(true);

		return isSuccess ? 0 : 1;
	}

	public static void main(String[] args) throws Exception {

		Configuration configuration = new Configuration();
		/**
		 args = new String[] { 
		 "hdfs://bskyey1:8020/tmp/input",
		 "hdfs://bskyey1:8020/tmp/output2" };
		 * 
		 * // run job int status = new WordCount2().run(args);
		 * 
		 * System.exit(status);
		 */
		// run job
		int status = ToolRunner.run(configuration, new WordCount2(), args);
		// exit program
		System.exit(status);
	}
}
