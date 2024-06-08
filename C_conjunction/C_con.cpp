#include <string>
#include<fstream>
#include "python.h" 

static PyObject *

spam_createFile(PyObject *self, PyObject *args)
{
	PyObject* listObj;

	if (!PyArg_ParseTuple(args, "O", &listObj))
		return NULL;

	if (!PyList_Check(listObj)) {
		PyErr_SetString(PyExc_TypeError, "Parameter must be a list");
		return NULL;
	}

	int listSize = PyList_Size(listObj);
	std::ofstream out{ "캐릭터 정보.txt" };
	for (int i = 0; i < listSize; ++i) {
		PyObject* item = PyList_GetItem(listObj, i);
		if (!PyUnicode_Check(item)) {
			PyErr_SetString(PyExc_TypeError, "List must contain only strings");
			return NULL;
		}
		const char* str = PyUnicode_AsUTF8(item);
		out << str << std::endl;
	}

	return Py_BuildValue("i", 0);
}

static PyMethodDef SpamMethods[] = {
	{ "createFile", spam_createFile, METH_VARARGS,
	"createFile for character" },
	{ NULL, NULL, 0, NULL } // 배열의 끝을 나타냅니다.
};

static struct PyModuleDef spammodule = {
	PyModuleDef_HEAD_INIT,
	"spam",            // 모듈 이름
	"It is test module.", // 모듈 설명을 적는 부분, 모듈의 __doc__에 저장됩니다.
	-1,SpamMethods
};

PyMODINIT_FUNC
PyInit_spam(void)
{
	return PyModule_Create(&spammodule);
}
