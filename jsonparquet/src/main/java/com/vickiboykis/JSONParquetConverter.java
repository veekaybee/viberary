package com.vickiboykis;

import org.apache.avro.Schema;
import org.apache.parquet.hadoop.ParquetWriter;
import org.apache.parquet.hadoop.metadata.CompressionCodecName;
import org.kitesdk.data.spi.JsonUtil;
import org.kitesdk.data.spi.filesystem.JSONFileReader;
import org.apache.parquet.avro.AvroParquetWriter;
import java.io.*;

import org.apache.hadoop.fs.Path;

import java.net.URL;

import static java.nio.file.Paths.*;
import static org.apache.avro.generic.GenericData.Record;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;

/**
 * Converts a JSON file to Parquet using an Avro schema
 *
 */
public class JSONParquetConverter
{


    public static Schema getAvroSchema(java.nio.file.Path path, String schemaName) throws IOException {
        String jsonString = Files.readString(path, StandardCharsets.UTF_8);
        return JsonUtil.inferSchema(JsonUtil.parse(jsonString), schemaName);
    }

    public static String readFileAsString(String file)throws Exception
    {
        return new String(Files.readAllBytes(get(file)));
    }


    public static <T> void main(String[] args ) throws Exception {

        InputStream sampleStream = JSONParquetConverter.class.getClassLoader().getResourceAsStream("goodreads_sample.json");
        InputStream totalStream = JSONParquetConverter.class.getClassLoader().getResourceAsStream("goodreads_books.json");
        String jsonString = new String(sampleStream.readAllBytes(), StandardCharsets.UTF_8);

        // Load schema
        URL resource = JSONParquetConverter.class.getResource("/goodreads.avsc");
        java.nio.file.Path schemaPath = get(resource.toURI());

        // Output path
        Path outputPath = new Path("goodreads_books.parquet");

        Schema schema = getAvroSchema(schemaPath, "mySchema");
        System.out.println(schema);

        try (JSONFileReader<Record> reader = new JSONFileReader<>(
                sampleStream, schema, Record.class)) {

            reader.initialize();

            long count = 0;

            try (ParquetWriter<Record> writer = AvroParquetWriter
                    .<Record>builder(outputPath)
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
