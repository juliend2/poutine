CREATE TABLE `questions` (
  `id` int(11) NOT NULL auto_increment,
  `question` varchar(250) NOT NULL,
  `sorting` int(11) default NULL,
  `created` datetime NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `answers` (
  `id` int(11) NOT NULL auto_increment,
  `answer_link` varchar(250) NULL,
  `answer_text` text NULL,
  `sorting` int(11) default NULL,
  `question_id` int(11) NOT NULL,
  `created` datetime NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

