# Installation

## Database

A mysql database needs to be setup with the following tables

```sql
CREATE TABLE `users` (
`id` int(16) DEFAULT NULL,
`password` varchar(150) DEFAULT NULL,
`email_verified` tinyint(2) DEFAULT 0,
`account_created` datetime DEFAULT NULL,
`sessions` varchar(200) DEFAULT '[]',
`phone_verified` tinyint(2) DEFAULT 0,
`organisation` int(10) DEFAULT NULL,
`designation` varchar(100) DEFAULT NULL,
`admin` tinyint(3) DEFAULT NULL,
`employ_id` int(10) DEFAULT NULL,
`name` varchar(100) DEFAULT NULL,
`email` varchar(100) DEFAULT NULL,
`phone` varchar(16) DEFAULT NULL,
`department` varchar(200) DEFAULT NULL,
`manager` int(16) DEFAULT NULL,
`country` varchar(100) DEFAULT NULL,
`city` varchar(100) DEFAULT NULL
);


CREATE TABLE `cache` (
  `namespace` varchar(50) NOT NULL,
  `key` varchar(500) NOT NULL,
  `value` varchar(500) DEFAULT NULL
);

CREATE TABLE `organisations` (
  `id` int(10) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `Country` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
```
