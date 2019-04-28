create table if not exists Category(
    `cateid` int(11) NOT NULL AUTO_INCREMENT,
    `cname` varchar(50) NOT NULL,
    `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    primary key(`cateid`),
    unique key `cname` (`cname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table if not exists Novel(
    `nid` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL,
    `author` varchar(30) NOT NULL,
    `cateid` int(11),
    `wordcounts` int(11),
    `summary` text,
    `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `mark` varchar(100),
    primary key(`nid`),
    CONSTRAINT `novel_category_cateid` FOREIGN KEY (`cateid`) REFERENCES `Category` (`cateid`) on delete SET NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table if not exists Chapter(
    `cid` int(11) NOT NULL AUTO_INCREMENT,
    `title` varchar(100) NOT NULL,
    `cindex` int(11) NOT NULL,
    `nid` int(11) NOT NULL,
    `content` text,
    `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `mark` varchar(100),
    primary key(`cid`),
    CONSTRAINT `chapter_novel_nid` FOREIGN KEY (`nid`) REFERENCES `Novel` (`nid`) on delete SET NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
insert into Category(cname) values("玄幻");
insert into Category(cname) values("修真");
insert into Category(cname) values("都市");
insert into Category(cname) values("穿越");
insert into Category(cname) values("网游");
insert into Category(cname) values("科幻");
insert into Category(cname) values("其他");
insert into Category(cname) values("排行榜");
insert into Category(cname) values("全本");
