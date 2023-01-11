package com.vickiboykis;

import org.apache.avro.Schema;
import org.apache.parquet.hadoop.ParquetWriter;
import org.apache.parquet.hadoop.metadata.CompressionCodecName;
import org.kitesdk.data.spi.JsonUtil;
import org.kitesdk.data.spi.filesystem.JSONFileReader;
import org.apache.parquet.avro.AvroParquetWriter;
import java.io.*;

import org.apache.hadoop.fs.Path;

import java.net.URI;
import java.net.URL;

import static java.nio.file.Paths.*;
import static org.apache.avro.generic.GenericData.Record;

import java.nio.charset.StandardCharsets;
import java.nio.file.*;

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

        // Output Hadoop filepath
        Path outputPath = new Path("goodreads_books.parquet");

        java.nio.file.Path outputLocalPath = new java.nio.file.Path("goodreads_books.parquet") {
            @Override
            public FileSystem getFileSystem() {
                return null;
            }

            @Override
            public boolean isAbsolute() {
                return false;
            }

            @Override
            public java.nio.file.Path getRoot() {
                return null;
            }

            @Override
            public java.nio.file.Path getFileName() {
                return null;
            }

            @Override
            public java.nio.file.Path getParent() {
                return null;
            }

            @Override
            public int getNameCount() {
                return 0;
            }

            @Override
            public java.nio.file.Path getName(int index) {
                return null;
            }

            @Override
            public java.nio.file.Path subpath(int beginIndex, int endIndex) {
                return null;
            }

            @Override
            public boolean startsWith(java.nio.file.Path other) {
                return false;
            }

            @Override
            public boolean endsWith(java.nio.file.Path other) {
                return false;
            }

            @Override
            public java.nio.file.Path normalize() {
                return null;
            }

            @Override
            public java.nio.file.Path resolve(java.nio.file.Path other) {
                return null;
            }

            @Override
            public java.nio.file.Path relativize(java.nio.file.Path other) {
                return null;
            }

            @Override
            public URI toUri() {
                return null;
            }

            @Override
            public java.nio.file.Path toAbsolutePath() {
                return null;
            }

            @Override
            public java.nio.file.Path toRealPath(LinkOption... options) throws IOException {
                return null;
            }

            @Override
            public WatchKey register(WatchService watcher, WatchEvent.Kind<?>[] events, WatchEvent.Modifier... modifiers) throws IOException {
                return null;
            }

            @Override
            public int compareTo(java.nio.file.Path other) {
                return 0;
            }
        };

        Schema schema = getAvroSchema(schemaPath, "mySchema");
        System.out.println(schema);

        Files.deleteIfExists("goodreads_books.parquet");

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
