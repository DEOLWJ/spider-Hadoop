package rank;

import java.io.IOException;
import java.text.SimpleDateFormat;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.jobcontrol.ControlledJob;
import org.apache.hadoop.mapreduce.lib.jobcontrol.JobControl;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.commons.io.FileUtils;
import java.io.File;


public class get_info {

	private static Path src_path = new Path("D:\\PythonProject\\spider\\popular\\popular_rank.csv");
	private static Path name_output_path = new Path("D:\\PythonProject\\spider\\hadoop\\name");
	private static Path type_output_path = new Path("D:\\PythonProject\\spider\\hadoop\\type");
	
	public static class NameMapper 
    extends Mapper<Object, Text, Text, IntWritable>{
 
		private final static IntWritable one = new IntWritable(1);
		private Text word = new Text();
   
		public void map(Object key, Text value, Context context
                 ) throws IOException, InterruptedException {
		 	//分割
		 	String[]  file = value.toString().split("\t");
		 	//取出视频的名称
		 	word.set(file[0]);
		 	context.write(word, one);
		}
	}
	
	public static class TypeMapper 
       extends Mapper<Object, Text, Text, IntWritable>{
    
    private final static IntWritable one = new IntWritable(1);
    private Text word = new Text();
      
    public void map(Object key, Text value, Context context
                    ) throws IOException, InterruptedException {
    	//分割
    	String[]  file = value.toString().split("\t");
    	//取出视频的类型
    	word.set(file[2]);
    	context.write(word, one);
    	}
	}
	
	public static class TypeSumReducer extends Reducer<Text,IntWritable,Text,IntWritable> {
		private IntWritable result = new IntWritable();
	
		public void reduce(Text key, Iterable<IntWritable> values, 
	                    Context context
	                    ) throws IOException, InterruptedException {
		    int sum = 0;
		    for (IntWritable val : values) {
		    	//计算评分和
			    sum += val.get();
			}
			result.set(sum);
			context.write(key, result);
		}
	}

	public static void main(String[] args) throws Exception {
		File name= new File(name_output_path.toString());
        try {
            FileUtils.deleteDirectory(name);
        } catch (IOException e) {
            e.printStackTrace();
        }
        
        File type= new File(type_output_path.toString());
        try {
            FileUtils.deleteDirectory(type);
        } catch (IOException e) {
            e.printStackTrace();
        }
		
		Configuration conf = new Configuration();
		
		Job job0 = Job.getInstance(conf, "name");
	    job0.setJarByClass(get_info.class);
	    job0.setMapperClass(NameMapper.class);
	    job0.setNumReduceTasks(0);
	    job0.setOutputKeyClass(Text.class);
	    job0.setOutputValueClass(IntWritable.class);
	    
	    FileInputFormat.addInputPath(job0, src_path);
	    FileOutputFormat.setOutputPath(job0,name_output_path);
		
		
		Job job1 = Job.getInstance(conf, "type");
	    job1.setJarByClass(get_info.class);
	    job1.setMapperClass(TypeMapper.class);
	    job1.setCombinerClass(TypeSumReducer.class);
	    job1.setReducerClass(TypeSumReducer.class);
	    job1.setOutputKeyClass(Text.class);
	    job1.setOutputValueClass(IntWritable.class);
	    
	    FileInputFormat.addInputPath(job1, src_path);
	    FileOutputFormat.setOutputPath(job1,type_output_path);
	    
	    ControlledJob controlledJob0=new ControlledJob(job0.getConfiguration());
	    ControlledJob controlledJob1=new ControlledJob(job1.getConfiguration());
	    
	    controlledJob0.setJob(job0);
	    controlledJob1.setJob(job1);
	    
	    JobControl jc=new JobControl("jc");
	    
	    jc.addJob(controlledJob0);
	    jc.addJob(controlledJob1);
	    
	    Thread jcThread = new Thread(jc);
	    jcThread.start();
	    while(true){
	        //当job池里所有的job完成后,执行 下一步操作
	        if(jc.allFinished()){
	            jc.stop();
	            System.exit(0);
	        }
	        //获取执行失败的job列表
	        if(jc.getFailedJobList().size() > 0){
	            jc.stop();
	            System.exit(0);
	        }
	    }
  }
}
