"""Read stage042 declared source/data and saved code without generating target code."""
import hashlib
import struct

MAGIC = 83 * 65536 + 70 * 256 + 50
EXEZ = 90 * 65536 + 69 * 256 + 88
TRANSPORT = 36864
PACKMAGIC = 80 * 65536 + 75 * 256 + 51
PERSISTMAX = 26 * 32768


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def checksum(image):
    value = 5381
    for offset, byte in enumerate(image):
        if offset < 24 or offset > 27:
            value = (value * 33 + byte) & 0xffffffff
    return value


def filesystem(disk):
    physical = disk[TRANSPORT:TRANSPORT + PERSISTMAX]
    if int.from_bytes(physical[:4], 'little') == PACKMAGIC:
        encoded_length = int.from_bytes(physical[4:8], 'little')
        assert 4 <= encoded_length <= PERSISTMAX - 8
        image = decode(physical[8:8 + encoded_length])
    else:
        size = int.from_bytes(physical[12:16], 'little')
        image = physical[:size]
    header = struct.unpack_from('<7I', image)
    magic, version, count, size, code_max, file_max, expected = header
    assert magic == MAGIC and version == 2 and count == 128
    assert len(image) == size
    assert checksum(image) == expected
    result = {}
    extents = []
    for index in range(count):
        width, length, offset, capacity = struct.unpack_from('<4I', image, 64 + index * 64)
        if not width:
            continue
        assert 0 < width <= 47 and length <= capacity <= file_max
        assert offset + capacity <= size - 9216
        name = image[80 + index * 64:80 + index * 64 + width].decode()
        assert name not in result
        result[name] = image[9216 + offset:9216 + offset + length]
        if capacity:
            extents.append((offset, offset + capacity, name))
    extents.sort()
    for previous, following in zip(extents, extents[1:]):
        assert previous[1] <= following[0], (previous, following)
    return result, {'size': size, 'code_max': code_max, 'file_max': file_max, 'files': count}


def decode(data):
    size = int.from_bytes(data[:4], 'little')
    out = bytearray()
    at = 4
    while len(out) < size:
        tag = data[at]
        at += 1
        if tag < 128:
            length = tag + 1
            out.extend(data[at:at + length])
            at += length
        else:
            length = tag - 128 + 3
            distance = int.from_bytes(data[at:at + 2], 'little')
            at += 2
            assert 0 < distance <= len(out)
            for _ in range(length):
                out.append(out[-distance])
    assert len(out) == size and at == len(data)
    return bytes(out)


def archive(data):
    entries = {}
    at = 0
    while data[at]:
        width = data[at]
        length = int.from_bytes(data[at + 1:at + 3], 'little')
        name = data[at + 3:at + 3 + width].decode()
        at += 3 + width
        assert name not in entries and at + length < len(data)
        entries[name] = data[at:at + length]
        at += length
    assert at == len(data) - 1
    return entries


def executable(data, capacity, magic=EXEZ):
    if int.from_bytes(data[:4], 'little') == magic:
        data = decode(data[4:])
    length = int.from_bytes(data[:4], 'little')
    assert 4 <= length <= capacity and length % 4 == 0 and len(data) == length + 4
    return data[4:]
