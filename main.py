import src.compressor as c
import src.purger as p
import asyncio

original_file = 'campus_original.kml'
compressed_file_name = asyncio.run(c.compress_kml(original_file))
p.purge_kml(compressed_file_name)

