from __init__ import CURSOR, CONN
from department import Department
from employee import Employee


class Review:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, year, summary, employee_id, id=None):
        self.id = id
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def __repr__(self):
        return (
            f"<Review {self.id}: {self.year}, {self.summary}, "
            + f"Employee: {self.employee_id}>"
        )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Review instances """
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            year INT,
            summary TEXT,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employee(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Review  instances """
        sql = """
            DROP TABLE IF EXISTS reviews;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the year, summary, and employee id values of the current Review object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""

        sql = '''
              INSERT (year, summary, employee_id) VALUES (?,?,?)
              '''
        CURSOR.execute(sql,(self.year,self.summary,self.employee_id))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self


    @classmethod
    def create(cls, year, summary, employee_id):
        """ Initialize a new Review instance and save the object to the database. Return the new instance. """
        instance = cls(year,summary, employee_id)
        instance.save()
        return instance
    
    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, new_year):
        if isinstance(new_year, int) and new_year >= 2000:
            self._year = new_year
        else:
            raise ValueError(
                "year must be an integer greater than or equla to 2000"
            )
    

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, summary):
        if isinstance(summary, str) and len(summary) > 0:
            self._summary = summary
        else:
            raise ValueError(
                "summary must be a non-empty string"
            )
        
    @property 
    def employee_id(self):
        return self._employee_id
    
    @employee_id.setter
    def employee_id(self,employee_id):
        if isinstance(employee_id, int) and Employee.find_by_id(employee_id):
            self._employee_id = employee_id
        else:
            raise ValueError('employee must be an integer that has been persisted to the database')
    
    

    

   
    
   

    

    
    

    

    # A review includes an attribute for the year as well as a summary of
    #  the employee's performance.

    # The instance method save() should persist the Review object to the "reviews" table:

    # Insert a new row with the year, summary, and employee_id values of the currentReview instance.
    # Update the object id attribute using the primary key value of new row.
    # Save the object in local dictionary using table row's PK as dictionary key.
    
    def save(self):
        sql = '''
              INSERT INTO reviews (year,summary, employee_id)
              VALUES (?,?,?)
              '''
        CURSOR.execute(sql,(self.year,self.summary,self.employee_id))
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self
        

    # This is a class method (create) that should:

    # Create a new Review instance using the parameter values.
    # Save the new Review instance to the "reviews" table.
    # Return the new Review instance.
    
    # self, year, summary, employee_id, id=None
    @classmethod
    def create(cls,year,summary,employee_id):
        review = cls(year,summary,employee_id)
        review.save()
        return review
    
    
    @classmethod
    # This class method should return a Review instance having the attribute values 
    # from the table row. You should check the dictionary for an existing instance 
    # using the row's primary key, and set the instance attributes to the row data 
    # if found. If the dictionary does not contain a previously persisted object with 
    # that id, create a new Review instance from the row data and add it to the dictionary. 
    # The method should return the cached object.

    # takes a given row (record) returns the corresponding instance
    # use the row's primary key check if the given primary key is in the all class attribute
    # if it is the update if not then make a new instance with the attributes from the record
    # and add the new instance to all after getting its id
    # return the new cached object

    def instance_from_db(cls,row):
        
       
        
        if row[0] in cls.all:
            instance = cls.all.get(row[0])
            instance.id = row[0]
            instance.year = row[1]
            instance.summary = row[2]
            instance.employee_id = row[3]
        else:
            instance = cls(row[1],row[2],row[3])
            cls.all[instance.id] = instance
        return instance

    # This class method takes in an id as a parameter, and should return a single 
    # Review instance corresponding to the row in the "reviews" table with that same id, 
    # or None is no such row exists in the table.

    @classmethod
    def find_by_id(cls,id):
        sql = '''
              SELECT * FROM reviews WHERE id = ?
              '''
       
        CURSOR.execute(sql,(id,))
        row = CURSOR.fetchone()
        return cls.all.get(id) if row else None
    
    
    # This instance method should update the year, summary and 
    # employee_id columns for a "reviews" table row based on the id of the current object.
    
    def update(self):
        sql = '''
              UPDATE reviews SET year = ?, summary = ?, employee_id = ? WHERE id = ?
              '''
        CURSOR.execute(sql,(self.year,self.summary,self.employee_id,self.id))
        CONN.commit()
    
 
    #  This instance method should delete a "reviews" table row based on the id of 
    # the current object. It will also remove the instance from the all dictionary 
    # and set the current object's id attribute to None.
    
   
    def delete(self):
        sql = '''
               DELETE FROM departments WHERE id = ?
              '''
        CURSOR.execute(sql,(self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id = None
    


    # This class method should return a list of Review instances for every row in the "reviews" table.
    # You can test your methods by running the tests in the "lib/testing/review_orm_test.py"
    # file:
    # get_all()
        
    @classmethod
    def get_all(cls):
        sql = '''
              SELECT * from reviews
              '''
        rows = CURSOR.execute(sql).fetchall()
        reviews = []
        for row in rows:
            if row[0] in cls.all:
                review = cls.all[row[0]]
                reviews.append(review)
            else:
                review = cls(row[0], row[1], row[2])
                reviews.append(review)

        return reviews
    
        
    



    






        



