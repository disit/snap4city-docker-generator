CREATE DATABASE filemanagerdb;

USE filemanagerdb;

CREATE TABLE fileextensions (
`id` INT NOT NULL AUTO_INCREMENT,
extension VARCHAR(30) NOT NULL,
PRIMARY KEY (`id`));

INSERT INTO fileextensions (extension) VALUES ("img");
INSERT INTO fileextensions (extension) VALUES ("png");
INSERT INTO fileextensions (extension) VALUES ("jpg");
INSERT INTO fileextensions (extension) VALUES ("pdf");
INSERT INTO fileextensions (extension) VALUES ("ps");
INSERT INTO fileextensions (extension) VALUES ("zip");
INSERT INTO fileextensions (extension) VALUES ("rar");
INSERT INTO fileextensions (extension) VALUES ("tgz");
INSERT INTO fileextensions (extension) VALUES ("doc");
INSERT INTO fileextensions (extension) VALUES ("docx");
INSERT INTO fileextensions (extension) VALUES ("xls");
INSERT INTO fileextensions (extension) VALUES ("xlsx");
INSERT INTO fileextensions (extension) VALUES ("ppt");
INSERT INTO fileextensions (extension) VALUES ("pptx");
INSERT INTO fileextensions (extension) VALUES ("tar");
INSERT INTO fileextensions (extension) VALUES ("pcx");
INSERT INTO fileextensions (extension) VALUES ("html");
INSERT INTO fileextensions (extension) VALUES ("css");
INSERT INTO fileextensions (extension) VALUES ("dat");
INSERT INTO fileextensions (extension) VALUES ("py");
INSERT INTO fileextensions (extension) VALUES ("r");
