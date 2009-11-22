CREATE TABLE `questions` (
  `id` int(11) NOT NULL auto_increment,
  `question` varchar(250) NOT NULL,
  `sorting` int(11) default NULL,
  `created` datetime NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

