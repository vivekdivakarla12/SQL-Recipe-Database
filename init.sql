CREATE DATABASE IF NOT EXISTS nu_recipes;

SET FOREIGN_KEY_CHECKS = 0;

USE nu_recipes;
SET GLOBAL log_bin_trust_function_creators = 1;

DROP TABLE IF EXISTS `restaurant`;
CREATE TABLE IF NOT EXISTS `restaurant`
(
  restaurant_id     INT PRIMARY KEY AUTO_INCREMENT,
  name              VARCHAR(64) NOT NULL,
  location          VARCHAR(64) NOT NULL,
  years_in_business INT DEFAULT NULL
);

DROP TABLE IF EXISTS `chef`;
CREATE TABLE IF NOT EXISTS `chef`
(
  chef_id    INT PRIMARY KEY AUTO_INCREMENT,
  username   VARCHAR(16) NOT NULL UNIQUE, # this is considered as a secondary index
  password   VARCHAR(32) NOT NULL,
  first_name VARCHAR(16)  DEFAULT NULL,
  last_name  VARCHAR(16)  DEFAULT NULL,
  bio        VARCHAR(256) DEFAULT NULL,
  location   VARCHAR(64)  DEFAULT NULL
);



DROP TABLE IF EXISTS `gourmet_chef`;
CREATE TABLE IF NOT EXISTS `gourmet_chef`
(
  gourmet_chef_id     INT PRIMARY KEY AUTO_INCREMENT,
  chef_id             INT NOT NULL,
  restaurant_id       INT DEFAULT NULL,
  years_of_experience INT DEFAULT NULL,
  FOREIGN KEY (chef_id)
    REFERENCES chef (chef_id)
    ON UPDATE NO ACTION
    ON DELETE CASCADE,
  FOREIGN KEY (restaurant_id)
    REFERENCES restaurant (restaurant_id)
    ON UPDATE NO ACTION
    ON DELETE CASCADE
);

DROP TABLE IF EXISTS `menu`;
CREATE TABLE IF NOT EXISTS `menu`
(
  menu_id       INT PRIMARY KEY AUTO_INCREMENT,
  chef_username VARCHAR(16) NOT NULL,
  name          VARCHAR(32) NOT NULL,
  keyword       VARCHAR(64) DEFAULT NULL,
  visibility    BOOL        DEFAULT TRUE,
  FOREIGN KEY (chef_username)
    REFERENCES chef (username)
    ON UPDATE NO ACTION
    ON DELETE CASCADE
);

DROP TABLE IF EXISTS `ingredient`;
CREATE TABLE IF NOT EXISTS `ingredient`
(
  ingredient_id INT PRIMARY KEY AUTO_INCREMENT,
  price         DECIMAL(6, 2) DEFAULT NULL,
  name          VARCHAR(64) NOT NULL UNIQUE
);

DROP TABLE IF EXISTS `recipe`;
CREATE TABLE IF NOT EXISTS `recipe`
(
  recipe_id             INT PRIMARY KEY AUTO_INCREMENT,
  name                  VARCHAR(64)   NOT NULL UNIQUE, # this is considered a secondary index
  author_id             INT           NOT NULL,
  serving_size          INT           NOT NULL,
  total_price           DECIMAL(8, 2) DEFAULT NULL,
  time_to_cook          INT           DEFAULT NULL, # in minutes
  directions            VARCHAR(2560) NOT NULL,
  verified              BOOLEAN       DEFAULT FALSE,
  published_at          TIMESTAMP     DEFAULT NOW(),
  rating                DECIMAL(2, 1) DEFAULT NULL,
  number_of_chefs_rated INT           DEFAULT 0,
  picture_url           VARCHAR(256)  DEFAULT NULL,
  notes                 VARCHAR(256)  DEFAULT NULL,
  dietary_restrictions  VARCHAR(256)  DEFAULT NULL,
  FOREIGN KEY (author_id)
    REFERENCES chef (chef_id)
    ON UPDATE NO ACTION
    ON DELETE CASCADE
);

DROP TABLE IF EXISTS `recipe_has_ingredient`;
CREATE TABLE IF NOT EXISTS `recipe_has_ingredient`
(
  recipe_ingredient_id INT PRIMARY KEY AUTO_INCREMENT,
  recipe_id            INT NOT NULL,
  ingredient_id        INT NOT NULL,
  FOREIGN KEY (recipe_id)
    REFERENCES recipe (recipe_id)
    ON UPDATE NO ACTION
    ON DELETE CASCADE,
  FOREIGN KEY (ingredient_id)
    REFERENCES ingredient (ingredient_id)
    ON UPDATE NO ACTION
    ON DELETE CASCADE
);

DROP TABLE IF EXISTS `menu_has_recipe`;
CREATE TABLE IF NOT EXISTS `menu_has_recipe`
(
  menu_recipe_id INT PRIMARY KEY AUTO_INCREMENT,
  recipe_id      INT NOT NULL,
  menu_id        INT NOT NULL,
  FOREIGN KEY (recipe_id)
    REFERENCES recipe (recipe_id)
    ON UPDATE NO ACTION
    ON DELETE CASCADE,
  FOREIGN KEY (menu_id)
    REFERENCES menu (menu_id)
    ON UPDATE NO ACTION
    ON DELETE CASCADE
);

DROP TABLE IF EXISTS `review`;
CREATE TABLE IF NOT EXISTS `review`
(
  review_id INT PRIMARY KEY AUTO_INCREMENT,
  title     VARCHAR(32)  NOT NULL,
  feedback  VARCHAR(256) NOT NULL
);

DROP TABLE IF EXISTS `review_recipe`;
CREATE TABLE IF NOT EXISTS `review_recipe`
(
  review_recipe_id INT PRIMARY KEY AUTO_INCREMENT,
  chef_id          INT NOT NULL,
  recipe_id        INT NOT NULL,
  review_id        INT NOT NULL UNIQUE,
  FOREIGN KEY (chef_id)
    REFERENCES chef (chef_id)
    ON UPDATE NO ACTION
    ON DELETE CASCADE,
  FOREIGN KEY (recipe_id)
    REFERENCES recipe (recipe_id)
    ON UPDATE NO ACTION
    ON DELETE CASCADE,
  FOREIGN KEY (review_id)
    REFERENCES review (review_id)
    ON UPDATE NO ACTION
    ON DELETE CASCADE
);

/*
 Functions
 */
DELIMITER //
DROP FUNCTION IF EXISTS getPassword;
CREATE FUNCTION getPassword(uname VARCHAR(16))
  RETURNS VARCHAR(16)
BEGIN
  DECLARE op VARCHAR(16);

  SELECT password INTO op FROM chef WHERE uname = username;

  RETURN (op);
END //
DELIMITER ;

#SELECT getPassword('hello');

DELIMITER //
DROP FUNCTION IF EXISTS getChefID;
CREATE FUNCTION getChefID(uname VARCHAR(16))
  RETURNS INT
BEGIN
  DECLARE op INT;

  SELECT chef_id INTO op FROM chef WHERE username = uname;

  RETURN (op);
END //
DELIMITER ;

#SELECT getChefID('allenlin');

/*
 Procedures
 */
# Chef related
DELIMITER //
DROP PROCEDURE IF EXISTS newChef;
CREATE PROCEDURE newChef(uname VARCHAR(16), passw VARCHAR(16))
BEGIN
  INSERT INTO chef (username, password) VALUES (uname, passw);
END //
DELIMITER ;

#CALL newChef('hello', 'goodbye');

DELIMITER //
DROP PROCEDURE IF EXISTS getChefInfo;
CREATE PROCEDURE getChefInfo(uname VARCHAR(16))
BEGIN
  SELECT username, first_name, last_name, bio, location FROM chef WHERE username = uname;
END //
DELIMITER ;

#CALL getChefInfo('hello');

DELIMITER //
DROP PROCEDURE IF EXISTS updateChef;
CREATE PROCEDURE updateChef(uname VARCHAR(16), u_first_name VARCHAR(16), u_last_name VARCHAR(16), u_bio VARCHAR(256),
                            u_location VARCHAR(64))
BEGIN
  UPDATE chef
  SET first_name = IFNULL(u_first_name, first_name),
      last_name=IFNULL(u_last_name, last_name),
      bio=IFNULL(u_bio, bio),
      location=IFNULL(u_location, location)
  WHERE username = uname;
END //
DELIMITER ;


DELIMITER //
DROP PROCEDURE IF EXISTS removeChef;
CREATE PROCEDURE removeChef(u_name VARCHAR(16))
BEGIN
  DELETE FROM chef WHERE username = u_name;
END //
DELIMITER ;

#CALL removeChef('allenlin');

# Menu related
DELIMITER //
DROP PROCEDURE IF EXISTS newMenu;
CREATE PROCEDURE newMenu(u_name VARCHAR(16), m_name VARCHAR(32), m_keyword VARCHAR(64), m_visibility BOOL)
BEGIN
  INSERT INTO menu(chef_username, name, keyword, visibility) VALUES (u_name, m_name, m_keyword, m_visibility);
END //
DELIMITER ;

#CALL newMenu('hello', 'italian cuisine', 'italian', TRUE);

DELIMITER //
DROP PROCEDURE IF EXISTS getMenu;
CREATE PROCEDURE getMenu(u_name VARCHAR(16))
BEGIN
  SELECT chef_username, name, keyword FROM menu WHERE chef_username = u_name;
END //
DELIMITER ;

#CALL getMenu('hello', 'italian cuisine');

DELIMITER //
DROP PROCEDURE IF EXISTS updateMenu;
CREATE PROCEDURE updateMenu(uname VARCHAR(16), m_name VARCHAR(32), m_keyword VARCHAR(64), m_visibility BOOL)
BEGIN

  UPDATE menu
  SET name      = IFNULL(m_name, name),
      keyword=IFNULL(m_keyword, keyword),
      visibility=IFNULL(m_visibility, visibility)
  WHERE chef_username = uname;
END //
DELIMITER ;

DELIMITER //
DROP PROCEDURE IF EXISTS removeMenu;
CREATE PROCEDURE removeMenu(u_name VARCHAR(16), m_name VARCHAR(32))
BEGIN
  DELETE FROM menu WHERE chef_username = u_name AND name = m_name;
END //
DELIMITER ;

#CALL removeMenu('hello', 'italian cuisine');

DROP PROCEDURE IF EXISTS resetTable;
DELIMITER //
CREATE PROCEDURE resetTable()
BEGIN
  DROP TABLE IF EXISTS `review_recipe`;
  DROP TABLE IF EXISTS `review`;
  DROP TABLE IF EXISTS `menu_has_recipe`;
  DROP TABLE IF EXISTS `recipe_has_ingredient`;
  DROP TABLE IF EXISTS `recipe`;
  DROP TABLE IF EXISTS `ingredient`;
  DROP TABLE IF EXISTS `menu`;
  DROP TABLE IF EXISTS `gourmet_chef`;
  DROP TABLE IF EXISTS `restaurant`;
  DROP TABLE IF EXISTS `chef`;
END//
DELIMITER ;

#CALL resetTable();

DELIMITER //
DROP PROCEDURE IF EXISTS myRecipesList;
CREATE PROCEDURE myRecipesList(usern VARCHAR(50))
BEGIN
  SELECT name,
         serving_size,
         total_price,
         time_to_cook,
         directions,
         verified,
         rating,
         number_of_chefs_rated,
         notes,
         dietary_restrictions
  FROM chef
         JOIN recipe ON author_id = chef_id
  WHERE username = usern;
END //
DELIMITER ;

#CALL myRecipesList('DariusGarland');

DELIMITER //
DROP PROCEDURE IF EXISTS newRecipe;
CREATE PROCEDURE newRecipe(u_name VARCHAR(16), r_name VARCHAR(64), r_serving_size INT, r_directions VARCHAR(2560))
BEGIN
  DECLARE op INT;
  SET op = getChefID(u_name);

  INSERT INTO recipe(name, author_id, serving_size, directions)
  VALUES (r_name, op, r_serving_size, r_directions);
END //
DELIMITER ;

#CALL newRecipe('allenlin', 'taiwanese street food', 3, 'add boba to milk tea');

DELIMITER //
DROP PROCEDURE IF EXISTS updateRecipe;
CREATE PROCEDURE updateRecipe(u_name VARCHAR(16), r_name VARCHAR(64), r_serving_size INT, r_total_price DECIMAL(8, 2),
                              r_time INT, r_directions VARCHAR(2560), r_verified BOOLEAN, r_rating DECIMAL(2, 1),
                              r_no_chefs_rated INT,
                              r_picture_url VARCHAR(256), r_notes VARCHAR(256), r_restrictions VARCHAR(256))
BEGIN
  DECLARE op INT;
  SET op = getChefID(u_name);

  UPDATE recipe
  SET serving_size          = IFNULL(r_serving_size, serving_size),
      total_price           = IFNULL(r_total_price, total_price),
      time_to_cook          = IFNULL(r_time, time_to_cook),
      directions            = IFNULL(r_directions, directions),
      verified              = IFNULL(r_verified, verified),
      rating                = IFNULL(r_rating, rating),
      number_of_chefs_rated = IFNULL(r_no_chefs_rated, number_of_chefs_rated),
      picture_url           = IFNULL(r_picture_url, picture_url),
      notes                 = IFNULL(r_notes, notes),
      dietary_restrictions  = IFNULL(r_restrictions, dietary_restrictions)
  WHERE author_id = op
    AND NAME = r_name;
END //
DELIMITER ;

/*
CALL updateRecipe('allenlin', 'taiwanese street food', 4, 3.67, 3, NULL, NULL, NULL, NULL, NULL, 'soak the boba with
brown sugar syrup', NULL);
 */

DELIMITER //
DROP PROCEDURE IF EXISTS gourmetChefList;
CREATE PROCEDURE gourmetChefList()
BEGIN
  SELECT c.first_name,
         c.last_name,
         c.bio,
         c.location,
         g.years_of_experience,
         r.name,
         r.years_in_business,
         r.location
  FROM chef c
         LEFT JOIN gourmet_chef g ON c.chef_id = g.chef_id
         INNER JOIN restaurant r ON g.restaurant_id = r.restaurant_id;
END //
DELIMITER ;

#CALL gourmetChefList();
