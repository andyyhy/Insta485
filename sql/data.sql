PRAGMA foreign_keys = ON;
INSERT INTO users(username, fullname, email, filename, password)
VALUES
    ('andyyhy', 'Andy Yang','andyyhy@umich.edu', 'a4f5d827c31b6e790d105e2f6b9c84aef2134b56.jpg', 'sha512$2fd3293cab31484c8fd8a23a1812c18d$113acb4300474cdb5891e337eba0301940e3cc3164f1b5c0fb7979f7511f38617b4935848d3c4e9087197f0ac8a431a1b8bd984ca442c5276dbae83431cc5636'),
    ('kimj', 'Justin Kim','kimj@umich.edu', '5e98b207d12c3f47182a0b5e69f4c0bd7a102f9c.jpg', 'sha512$2fd3293cab31484c8fd8a23a1812c18d$113acb4300474cdb5891e337eba0301940e3cc3164f1b5c0fb7979f7511f38617b4935848d3c4e9087197f0ac8a431a1b8bd984ca442c5276dbae83431cc5636'),
    ('rodrid', ' Diego Rodriguez','rodrid@umich.edu', 'b74f21a5d09c87e01f2a3b6c4d5e78f012345678.jpg', 'sha512$2fd3293cab31484c8fd8a23a1812c18d$113acb4300474cdb5891e337eba0301940e3cc3164f1b5c0fb7979f7511f38617b4935848d3c4e9087197f0ac8a431a1b8bd984ca442c5276dbae83431cc5636'),
    ('athomps', 'Amelia Thompson','athomps@umich.edu', '01d2f3a45b6789c0e1f2a3b4c5d6e7f890a12b3c.jpg', 'sha512$2fd3293cab31484c8fd8a23a1812c18d$113acb4300474cdb5891e337eba0301940e3cc3164f1b5c0fb7979f7511f38617b4935848d3c4e9087197f0ac8a431a1b8bd984ca442c5276dbae83431cc5636'),
    ('ajackson', 'Andrew Jackson','ajackson@umich.edu', '6a7b8c9d0e1f2a3b4c5d6e7f01234567890abcd.jpg', 'sha512$2fd3293cab31484c8fd8a23a1812c18d$113acb4300474cdb5891e337eba0301940e3cc3164f1b5c0fb7979f7511f38617b4935848d3c4e9087197f0ac8a431a1b8bd984ca442c5276dbae83431cc5636');

INSERT INTO posts(filename, owner)
VALUES
    ('3a9d5f71820c6b4e7f8d0a1b2c3e5f607918d2c4.jpg', 'andyyhy'),
    ('f0b2a5c38d1e7946052138b9c7a4d6e5f0219347.jpg', 'kimj'),
    ('7a9b0c2d3e4f506178293a4b5c6d7e8f9012345b.jpg', 'andyyhy'),
    ('28f9d0a7b6c543219e8f7d6a5b4c309182e5f7b4.jpg', 'athomps'),
    ('7b9a5c830d1f2e49506a2138b4c7d5e6f0923147.jpg', 'athomps'),
    ('a9b8c7d6e5f40312569e8a7b6c5d4f3e20918273.jpg', 'ajackson'),
    ('9d8a0b2c3e4f5a61782930b4c5d6e7f8091234ab.jpg', 'rodrid'),
    ('5d6a7b8c9e0f1a234b5c6d7e890f2a3b4c5d8e9f.jpg', 'kimj'),
    ('a0b1c2d3e4f59876e7f8a9b0c1d2e3f4a567890b.jpg', 'andyyhy');

INSERT INTO following(username1, username2)
VALUES
    ('andyyhy', 'kimj'),
    ('andyyhy', 'rodrid'),
    ('athomps', 'andyyhy'),
    ('ajackson', 'athomps'),
    ('ajackson', 'andyyhy'),
    ('kimj', 'ajackson'),
    ('kimj', 'athomps');


INSERT INTO comments(owner, postid, text)
VALUES
    ('andyyhy','3','This is amazing!'),
    ('ajackson','3','Loving the vibes in this photo!'),
    ('rodrid','3','Such a beautiful moment captured!'),
    ('andyyhy','2','Your content is always so inspiring!'),
    ('ajackson','1','Wow, this is stunning! Where was this taken?'),
    ('andyyhy','1','This made my day!'),
    ('kimj','4','I cant get over how good this looks!');

INSERT INTO likes(owner, postid)
VALUES
    ('andyyhy','1'),
    ('ajackson','1'),
    ('rodrid','1'),
    ('andyyhy','2'),
    ('kimj','2'),
    ('andyyhy','3');