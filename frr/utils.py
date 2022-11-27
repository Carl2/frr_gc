"""Utility functions."""


def get_column_fn(rows):
    """Return a function which can get a specific column.

    The rows are [[a,b,c],[d,e,f]] so if choosing column 2
    the result would be [b,e]
    Keyword Arguments:
    rows -- Two dimensional list
    """
    def column_fn(*, clmn_num, apply_item=None, apply_list=None):
        """Return column based on previously defined list.

        Keyword Arguments:
        clmn_num -- coulmn number
        apply_item -- Apply function to each of the item
        apply_list -- Apply function to the complete list.


        example:
        rows = [[1,2,3],[4,5,6]]
        fn = utils.get_column_fn(rows)
        def avg(lst):
          return reduce(lambda a, b: a + b, lst) / len(lst)

        avg = fn(clmn_num=1,apply_item=lambda x: x*2,apply_list=avg )
        assert( avg == 7.0)
        """
        column = []
        if apply_item is None:
            column = [row[clmn_num] for row in rows]
        else:
            column = [apply_item(row[clmn_num]) for row in rows]

        if apply_list is None:
            return column
        else:
            return apply_list(column)

    return column_fn


def get_cols_row_fn(rows):
    """Return function which can be used to get columns.

    Keyword Arguments:
    rows        -- Rows of type [[1,2,3],[4,5,6]
    """

    def get_cols_row(*cols, apply_field=None, apply_list=None):
        """Return a list of tuples with the columns specified from the row.

        Keyword Arguments:
        *cols -- e.g 1,3
        row   -- [[a,b,c,d],[e,f,g,h]]
        apply_field -- (default None) Function to which one can apply transformation on field
        apply_list  -- (default None) Function to transform the complete list

        The above will return [[a,c],[e,g]]
        """
        #nonlocal apply_list
        def get_col_from_row(row):
            nonlocal apply_field
            if apply_field is None:
                return [row[col] for col in cols]
            else:
                return [apply_field(row[col]) for col in cols]

        vals = [get_col_from_row(row) for row in rows]
        if apply_list is None:
            return vals
        else:
            return apply_list(vals)
    return get_cols_row
