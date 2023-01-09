package com.vickiboykis;

import org.apache.avro.Schema;
import org.apache.parquet.hadoop.ParquetWriter;
import org.apache.parquet.hadoop.metadata.CompressionCodecName;
import org.apache.parquet.io.OutputFile;
import org.kitesdk.data.spi.JsonUtil;
import org.kitesdk.data.spi.filesystem.JSONFileReader;
import org.apache.parquet.avro.AvroParquetWriter;
import java.io.*;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import static org.apache.avro.generic.GenericData.Record;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

/**
 * Converts a JSON file to Parquet using an Avro schema
 *
 */
public class JSONParquetConverter
{

    public static Schema getAvroSchema(String jsonString, String schemaName) {
        return JsonUtil.inferSchema(JsonUtil.parse(jsonString), schemaName);
    }

    public static String readFileAsString(String file)throws Exception
    {
        return new String(Files.readAllBytes(Paths.get(file)));
    }

    public static <T> void main(String[] args ) throws Exception {

        InputStream sampleStream = JSONParquetConverter.class.getClassLoader().getResourceAsStream("goodreads_sample.json");
        InputStream totalStream = JSONParquetConverter.class.getClassLoader().getResourceAsStream("goodreads_books.json");
        String jsonString = new String(sampleStream.readAllBytes(), StandardCharsets.UTF_8);

        File outputPath = new File("/resources/goodreads_books.avro");

        Schema schema = getAvroSchema(jsonString, "mySchema");

        try (JSONFileReader<Record> reader = new JSONFileReader<>(
                totalStream, schema, Record.class)) {

            reader.initialize();

            long count = 0;

            try (ParquetWriter<Record> writer = AvroParquetWriter
                    .<Record>builder((OutputFile) outputPath)
                    .withCompressionCodec(CompressionCodecName.SNAPPY)
                    .withSchema(schema)
                    .build()) {
                for (Record record : reader) {
                    writer.write(record);
                    count += 1;
                    System.out.println(count + "rows converted");
                }
            }
        }
    }
}
