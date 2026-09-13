#include <algorithm>
#include <cmath>
#include <cstddef>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

namespace aqarion::sv001 {

using Matrix = std::vector<std::vector<double>>;

constexpr double kTolerance = 1.0e-12;

struct TestCase {
    std::size_t m;
    std::size_t k;
    std::size_t s;
    std::string name;
};

struct CheckResult {
    bool passed = false;
    std::size_t m = 0;
    std::size_t k = 0;
    std::size_t s = 0;
    std::size_t r = 0;
    double alpha_squared = 0.0;
    double gram_residual = 0.0;
    double spectrum_residual = 0.0;
    double zero_defect_residual = 0.0;
};

Matrix zeros(std::size_t rows, std::size_t cols) {
    return Matrix(rows, std::vector<double>(cols, 0.0));
}

Matrix identity(std::size_t n) {
    Matrix result = zeros(n, n);

    for (std::size_t i = 0; i < n; ++i) {
        result[i][i] = 1.0;
    }

    return result;
}

Matrix transpose(const Matrix& a) {
    if (a.empty()) {
        return {};
    }

    const std::size_t rows = a.size();
    const std::size_t cols = a.front().size();

    Matrix result = zeros(cols, rows);

    for (std::size_t i = 0; i < rows; ++i) {
        for (std::size_t j = 0; j < cols; ++j) {
            result[j][i] = a[i][j];
        }
    }

    return result;
}

Matrix add(const Matrix& a, const Matrix& b) {
    const std::size_t rows = a.size();
    const std::size_t cols = a.front().size();

    Matrix result = zeros(rows, cols);

    for (std::size_t i = 0; i < rows; ++i) {
        for (std::size_t j = 0; j < cols; ++j) {
            result[i][j] = a[i][j] + b[i][j];
        }
    }

    return result;
}

Matrix subtract(const Matrix& a, const Matrix& b) {
    const std::size_t rows = a.size();
    const std::size_t cols = a.front().size();

    Matrix result = zeros(rows, cols);

    for (std::size_t i = 0; i < rows; ++i) {
        for (std::size_t j = 0; j < cols; ++j) {
            result[i][j] = a[i][j] - b[i][j];
        }
    }

    return result;
}

Matrix scale(double scalar, const Matrix& a) {
    const std::size_t rows = a.size();
    const std::size_t cols = a.front().size();

    Matrix result = zeros(rows, cols);

    for (std::size_t i = 0; i < rows; ++i) {
        for (std::size_t j = 0; j < cols; ++j) {
            result[i][j] = scalar * a[i][j];
        }
    }

    return result;
}

Matrix multiply(const Matrix& a, const Matrix& b) {
    if (a.empty() || b.empty()) {
        return {};
    }

    const std::size_t a_rows = a.size();
    const std::size_t a_cols = a.front().size();
    const std::size_t b_rows = b.size();
    const std::size_t b_cols = b.front().size();

    if (a_cols != b_rows) {
        throw std::runtime_error("Matrix dimension mismatch in multiply.");
    }

    Matrix result = zeros(a_rows, b_cols);

    for (std::size_t i = 0; i < a_rows; ++i) {
        for (std::size_t k = 0; k < a_cols; ++k) {
            const double aik = a[i][k];

            if (aik == 0.0) {
                continue;
            }

            for (std::size_t j = 0; j < b_cols; ++j) {
                result[i][j] += aik * b[k][j];
            }
        }
    }

    return result;
}

double frobenius_norm(const Matrix& a) {
    double squared_sum = 0.0;

    for (const auto& row : a) {
        for (double value : row) {
            squared_sum += value * value;
        }
    }

    return std::sqrt(squared_sum);
}

double max_abs_entry(const Matrix& a) {
    double maximum = 0.0;

    for (const auto& row : a) {
        for (double value : row) {
            maximum = std::max(maximum, std::abs(value));
        }
    }

    return maximum;
}

bool is_near(double actual, double expected, double tolerance = kTolerance) {
    return std::abs(actual - expected) <= tolerance;
}

bool matrix_near(const Matrix& a,
                 const Matrix& b,
                 double tolerance = kTolerance) {
    if (a.size() != b.size()) {
        return false;
    }

    if (!a.empty() && a.front().size() != b.front().size()) {
        return false;
    }

    return frobenius_norm(subtract(a, b)) <= tolerance;
}

Matrix block_average_projection(std::size_t m, std::size_t k) {
    const std::size_t n = m * k;
    Matrix p = zeros(n, n);

    for (std::size_t block = 0; block < m; ++block) {
        const std::size_t begin = block * k;
        const std::size_t end = begin + k;

        for (std::size_t row = begin; row < end; ++row) {
            for (std::size_t col = begin; col < end; ++col) {
                p[row][col] = 1.0 / static_cast<double>(k);
            }
        }
    }

    return p;
}

Matrix koopman_shift(std::size_t n, std::size_t s) {
    Matrix k_shift = zeros(n, n);

    const std::size_t reduced_shift = s % n;

    for (std::size_t x = 0; x < n; ++x) {
        const std::size_t shifted_x = (x + reduced_shift) % n;
        k_shift[x][shifted_x] = 1.0;
    }

    return k_shift;
}

Matrix normalized_block_basis(std::size_t m, std::size_t k) {
    const std::size_t n = m * k;
    Matrix u = zeros(n, m);

    const double coefficient = 1.0 / std::sqrt(static_cast<double>(k));

    for (std::size_t block = 0; block < m; ++block) {
        const std::size_t begin = block * k;
        const std::size_t end = begin + k;

        for (std::size_t x = begin; x < end; ++x) {
            u[x][block] = coefficient;
        }
    }

    return u;
}

Matrix defect_operator(std::size_t m, std::size_t k, std::size_t s) {
    const std::size_t n = m * k;

    const Matrix i = identity(n);
    const Matrix p = block_average_projection(m, k);
    const Matrix k_shift = koopman_shift(n, s);

    return multiply(multiply(subtract(i, p), k_shift), p);
}

Matrix reduced_gram(std::size_t m, std::size_t k, std::size_t s) {
    const Matrix d = defect_operator(m, k, s);
    const Matrix u = normalized_block_basis(m, k);

    const Matrix dt = transpose(d);
    const Matrix ut = transpose(u);

    return multiply(multiply(multiply(ut, dt), d), u);
}

Matrix cycle_laplacian_multigraph(std::size_t m) {
    if (m < 2) {
        throw std::runtime_error(
            "cycle_laplacian_multigraph requires m >= 2."
        );
    }

    Matrix l = zeros(m, m);

    for (std::size_t i = 0; i < m; ++i) {
        const std::size_t plus_one = (i + 1) % m;
        const std::size_t minus_one = (i + m - 1) % m;

        l[i][i] += 2.0;
        l[i][plus_one] -= 1.0;
        l[i][minus_one] -= 1.0;
    }

    return l;
}

Matrix cycle_laplacian_wrong_simple_c2() {
    return {
        {2.0, -1.0},
        {-1.0, 2.0},
    };
}

Matrix expected_gram(std::size_t m,
                     std::size_t k,
                     std::size_t s) {
    const std::size_t r = s % k;

    if (r == 0) {
        return zeros(m, m);
    }

    const double r_as_double = static_cast<double>(r);
    const double k_as_double = static_cast<double>(k);

    const double alpha_squared =
        r_as_double * (k_as_double - r_as_double) /
        (k_as_double * k_as_double);

    return scale(alpha_squared, cycle_laplacian_multigraph(m));
}

std::vector<double> jacobi_eigenvalues_symmetric(Matrix a,
                                                  double tolerance = 1.0e-14,
                                                  std::size_t max_iterations = 100000) {
    const std::size_t n = a.size();

    if (n == 0) {
        return {};
    }

    for (const auto& row : a) {
        if (row.size() != n) {
            throw std::runtime_error(
                "Jacobi eigensolver requires a square matrix."
            );
        }
    }

    for (std::size_t iteration = 0; iteration < max_iterations; ++iteration) {
        std::size_t p = 0;
        std::size_t q = 0;
        double largest_off_diagonal = 0.0;

        for (std::size_t i = 0; i < n; ++i) {
            for (std::size_t j = i + 1; j < n; ++j) {
                const double candidate = std::abs(a[i][j]);

                if (candidate > largest_off_diagonal) {
                    largest_off_diagonal = candidate;
                    p = i;
                    q = j;
                }
            }
        }

        if (largest_off_diagonal <= tolerance) {
            break;
        }

        const double app = a[p][p];
        const double aqq = a[q][q];
        const double apq = a[p][q];

        const double angle =
            0.5 * std::atan2(2.0 * apq, aqq - app);

        const double c = std::cos(angle);
        const double s = std::sin(angle);

        for (std::size_t i = 0; i < n; ++i) {
            if (i == p || i == q) {
                continue;
            }

            const double aip = a[i][p];
            const double aiq = a[i][q];

            a[i][p] = c * aip - s * aiq;
            a[p][i] = a[i][p];

            a[i][q] = s * aip + c * aiq;
            a[q][i] = a[i][q];
        }

        a[p][p] =
            c * c * app - 2.0 * s * c * apq + s * s * aqq;

        a[q][q] =
            s * s * app + 2.0 * s * c * apq + c * c * aqq;

        a[p][q] = 0.0;
        a[q][p] = 0.0;
    }

    std::vector<double> eigenvalues(n);

    for (std::size_t i = 0; i < n; ++i) {
        eigenvalues[i] = a[i][i];
    }

    std::sort(eigenvalues.begin(), eigenvalues.end());

    return eigenvalues;
}

std::vector<double> expected_gram_eigenvalues(std::size_t m,
                                               std::size_t k,
                                               std::size_t s) {
    const std::size_t r = s % k;
    std::vector<double> result;

    if (r == 0) {
        result.assign(m, 0.0);
        return result;
    }

    const double r_as_double = static_cast<double>(r);
    const double k_as_double = static_cast<double>(k);

    const double alpha_squared =
        r_as_double * (k_as_double - r_as_double) /
        (k_as_double * k_as_double);

    for (std::size_t ell = 0; ell < m; ++ell) {
        const double angle =
            std::acos(-1.0) *
            static_cast<double>(ell) /
            static_cast<double>(m);

        result.push_back(
            4.0 * alpha_squared * std::sin(angle) * std::sin(angle)
        );
    }

    std::sort(result.begin(), result.end());

    return result;
}

double vector_l2_distance(const std::vector<double>& a,
                          const std::vector<double>& b) {
    if (a.size() != b.size()) {
        throw std::runtime_error(
            "Vector dimension mismatch in vector_l2_distance."
        );
    }

    double squared_sum = 0.0;

    for (std::size_t i = 0; i < a.size(); ++i) {
        const double difference = a[i] - b[i];
        squared_sum += difference * difference;
    }

    return std::sqrt(squared_sum);
}

CheckResult verify_case(std::size_t m,
                        std::size_t k,
                        std::size_t s,
                        double tolerance = kTolerance) {
    if (m < 2) {
        throw std::runtime_error("SV-001 requires m >= 2.");
    }

    if (k < 1) {
        throw std::runtime_error("SV-001 requires k >= 1.");
    }

    CheckResult result;
    result.m = m;
    result.k = k;
    result.s = s;
    result.r = s % k;

    const Matrix d = defect_operator(m, k, s);
    const Matrix g = reduced_gram(m, k, s);
    const Matrix target = expected_gram(m, k, s);

    if (result.r == 0) {
        result.zero_defect_residual = frobenius_norm(d);
        result.gram_residual = frobenius_norm(g);
        result.spectrum_residual = 0.0;
        result.passed = result.zero_defect_residual <= tolerance;
        return result;
    }

    const double r_as_double = static_cast<double>(result.r);
    const double k_as_double = static_cast<double>(k);

    result.alpha_squared =
        r_as_double * (k_as_double - r_as_double) /
        (k_as_double * k_as_double);

    result.gram_residual = frobenius_norm(subtract(g, target));

    const std::vector<double> actual_eigenvalues =
        jacobi_eigenvalues_symmetric(g);

    const std::vector<double> predicted_eigenvalues =
        expected_gram_eigenvalues(m, k, s);

    result.spectrum_residual =
        vector_l2_distance(actual_eigenvalues, predicted_eigenvalues);

    result.passed =
        result.gram_residual <= tolerance &&
        result.spectrum_residual <= tolerance;

    return result;
}

void print_matrix(const Matrix& matrix,
                  const std::string& name) {
    std::cout << name << ":
";

    std::cout << std::fixed << std::setprecision(12);

    for (const auto& row : matrix) {
        std::cout << "  [";

        for (std::size_t j = 0; j < row.size(); ++j) {
            std::cout << std::setw(16) << row[j];

            if (j + 1 < row.size()) {
                std::cout << ", ";
            }
        }

        std::cout << "]
";
    }
}

void print_case_result(const TestCase& test_case,
                       const CheckResult& result) {
    std::cout
        << "[" << (result.passed ? "PASS" : "FAIL") << "] "
        << test_case.name
        << "  m=" << result.m
        << " k=" << result.k
        << " s=" << result.s
        << " r=" << result.r;

    if (result.r == 0) {
        std::cout
            << " zero_defect_residual="
            << std::scientific << std::setprecision(6)
            << result.zero_defect_residual
            << "
";
        return;
    }

    std::cout
        << " alpha2="
        << std::scientific << std::setprecision(6)
        << result.alpha_squared
        << " gram_residual="
        << result.gram_residual
        << " spectrum_residual="
        << result.spectrum_residual
        << "
";
}

bool test_cycle_laplacian_m2() {
    const Matrix actual = cycle_laplacian_multigraph(2);

    const Matrix expected = {
        {2.0, -2.0},
        {-2.0, 2.0},
    };

    const bool passed = matrix_near(actual, expected);

    std::cout
        << "[" << (passed ? "PASS" : "FAIL") << "] "
        << "SV001-M2-LAPLACIAN: "
        << "L(C_2^circ) must be the double-edge Laplacian.
";

    if (!passed) {
        print_matrix(actual, "actual L(C_2^circ)");
        print_matrix(expected, "expected L(C_2^circ)");
    }

    return passed;
}

bool test_cycle_laplacian_spectrum_m2() {
    const Matrix l = cycle_laplacian_multigraph(2);
    const std::vector<double> actual = jacobi_eigenvalues_symmetric(l);
    const std::vector<double> expected = {0.0, 4.0};

    const double residual = vector_l2_distance(actual, expected);
    const bool passed = residual <= kTolerance;

    std::cout
        << "[" << (passed ? "PASS" : "FAIL") << "] "
        << "SV001-M2-SPECTRUM: "
        << "eigenvalues of L(C_2^circ) are {0,4}; residual="
        << std::scientific << std::setprecision(6)
        << residual << "
";

    return passed;
}

bool test_wrong_simple_c2_negative_control() {
    const std::size_t m = 2;
    const std::size_t k = 3;
    const std::size_t s = 1;

    const std::size_t r = s % k;

    const double alpha_squared =
        static_cast<double>(r) *
        (static_cast<double>(k) - static_cast<double>(r)) /
        (static_cast<double>(k) * static_cast<double>(k));

    const Matrix g = reduced_gram(m, k, s);
    const Matrix wrong_target =
        scale(alpha_squared, cycle_laplacian_wrong_simple_c2());

    const Matrix correct_target =
        scale(alpha_squared, cycle_laplacian_multigraph(m));

    const double wrong_residual =
        frobenius_norm(subtract(g, wrong_target));

    const double correct_residual =
        frobenius_norm(subtract(g, correct_target));

    const bool passed =
        wrong_residual > 1.0e-6 &&
        correct_residual <= kTolerance;

    std::cout
        << "[" << (passed ? "PASS" : "FAIL") << "] "
        << "SV001-NEG-001: "
        << "wrong simple C_2 target residual="
        << std::scientific << std::setprecision(6)
        << wrong_residual
        << ", correct multigraph target residual="
        << correct_residual
        << "
";

    return passed;
}

bool test_block_basis_orthonormality() {
    const std::size_t m = 5;
    const std::size_t k = 4;

    const Matrix u = normalized_block_basis(m, k);
    const Matrix gram = multiply(transpose(u), u);
    const Matrix expected = identity(m);

    const double residual = frobenius_norm(subtract(gram, expected));
    const bool passed = residual <= kTolerance;

    std::cout
        << "[" << (passed ? "PASS" : "FAIL") << "] "
        << "SV001-BASIS-001: "
        << "U^T U = I; residual="
        << std::scientific << std::setprecision(6)
        << residual << "
";

    return passed;
}

bool test_projection_idempotence() {
    const std::size_t m = 4;
    const std::size_t k = 5;

    const Matrix p = block_average_projection(m, k);
    const Matrix p_squared = multiply(p, p);

    const double residual = frobenius_norm(subtract(p_squared, p));
    const bool passed = residual <= kTolerance;

    std::cout
        << "[" << (passed ? "PASS" : "FAIL") << "] "
        << "SV001-PROJECTION-001: "
        << "P^2 = P; residual="
        << std::scientific << std::setprecision(6)
        << residual << "
";

    return passed;
}

bool run_regression_cases() {
    const std::vector<TestCase> cases = {
        {2, 3, 1, "SV001-M2-001"},
        {2, 3, 2, "SV001-M2-002"},
        {2, 4, 2, "SV001-M2-003"},
        {3, 3, 1, "SV001-C3-001"},
        {3, 3, 2, "SV001-C3-002"},
        {3, 4, 2, "SV001-C3-003"},
        {3, 4, 5, "SV001-C3-004"},
        {4, 3, 2, "SV001-C4-001"},
        {4, 5, 3, "SV001-C4-002"},
        {5, 4, 2, "SV001-C5-001"},
        {3, 4, 4, "SV001-EQ-001"},
        {4, 5, 10, "SV001-EQ-002"},
    };

    bool all_passed = true;

    for (const TestCase& test_case : cases) {
        const CheckResult result =
            verify_case(test_case.m, test_case.k, test_case.s);

        print_case_result(test_case, result);
        all_passed = all_passed && result.passed;
    }

    return all_passed;
}

bool run_exhaustive_small() {
    constexpr std::size_t m_min = 2;
    constexpr std::size_t m_max = 8;
    constexpr std::size_t k_min = 2;
    constexpr std::size_t k_max = 8;

    std::size_t total = 0;
    std::size_t passed = 0;

    double largest_gram_residual = 0.0;
    double largest_spectrum_residual = 0.0;
    double largest_zero_defect_residual = 0.0;

    TestCase largest_gram_case{};
    TestCase largest_spectrum_case{};
    TestCase largest_zero_defect_case{};

    for (std::size_t m = m_min; m <= m_max; ++m) {
        for (std::size_t k = k_min; k <= k_max; ++k) {
            const std::size_t n = m * k;

            for (std::size_t s = 1; s < n; ++s) {
                ++total;

                const CheckResult result = verify_case(m, k, s);

                if (result.passed) {
                    ++passed;
                } else {
                    std::cout
                        << "[FAIL] SV001-EXH-001"
                        << " m=" << m
                        << " k=" << k
                        << " s=" << s
                        << " r=" << result.r
                        << " gram_residual="
                        << std::scientific << std::setprecision(12)
                        << result.gram_residual
                        << " spectrum_residual="
                        << result.spectrum_residual
                        << " zero_defect_residual="
                        << result.zero_defect_residual
                        << "
";
                }

                if (result.gram_residual > largest_gram_residual) {
                    largest_gram_residual = result.gram_residual;
                    largest_gram_case = {m, k, s, "largest_gram"};
                }

                if (result.spectrum_residual > largest_spectrum_residual) {
                    largest_spectrum_residual = result.spectrum_residual;
                    largest_spectrum_case = {m, k, s, "largest_spectrum"};
                }

                if (result.zero_defect_residual > largest_zero_defect_residual) {
                    largest_zero_defect_residual =
                        result.zero_defect_residual;

                    largest_zero_defect_case =
                        {m, k, s, "largest_zero_defect"};
                }
            }
        }
    }

    const bool all_passed = (total == passed);

    std::cout << "
";
    std::cout
        << "[" << (all_passed ? "PASS" : "FAIL") << "] "
        << "SV001-EXH-001"
        << " tested=" << total
        << " passed=" << passed
        << " m_range=[" << m_min << "," << m_max << "]"
        << " k_range=[" << k_min << "," << k_max << "]"
        << "
";

    std::cout
        << "largest_gram_residual="
        << std::scientific << std::setprecision(12)
        << largest_gram_residual
        << " at (m,k,s)=("
        << largest_gram_case.m << ","
        << largest_gram_case.k << ","
        << largest_gram_case.s << ")
";

    std::cout
        << "largest_spectrum_residual="
        << std::scientific << std::setprecision(12)
        << largest_spectrum_residual
        << " at (m,k,s)=("
        << largest_spectrum_case.m << ","
        << largest_spectrum_case.k << ","
        << largest_spectrum_case.s << ")
";

    std::cout
        << "largest_zero_defect_residual="
        << std::scientific << std::setprecision(12)
        << largest_zero_defect_residual
        << " at (m,k,s)=("
        << largest_zero_defect_case.m << ","
        << largest_zero_defect_case.k << ","
        << largest_zero_defect_case.s << ")
";

    return all_passed;
}

}  // namespace aqarion::sv001

int main() {
    using namespace aqarion::sv001;

    std::cout
        << "AQARION SV-001 reference numerical test
"
        << "Status: finite floating-point experiment only; "
        << "not a Lean certificate or formal proof.
"
        << "Tolerance: "
        << std::scientific << std::setprecision(3)
        << kTolerance << "

";

    bool all_passed = true;

    all_passed = test_cycle_laplacian_m2() && all_passed;
    all_passed = test_cycle_laplacian_spectrum_m2() && all_passed;
    all_passed = test_wrong_simple_c2_negative_control() && all_passed;
    all_passed = test_block_basis_orthonormality() && all_passed;
    all_passed = test_projection_idempotence() && all_passed;

    std::cout << "
=== Fixed regression cases ===
";
    all_passed = run_regression_cases() && all_passed;

    std::cout << "
=== Exhaustive small sweep ===
";
    all_passed = run_exhaustive_small() && all_passed;

    std::cout << "
";

    if (all_passed) {
        std::cout
            << "FINAL RESULT: PASS
"
            << "The tested finite cases match the specified multigraph "
            << "cycle-Laplacian target within the stated tolerance.
";

        return 0;
    }

    std::cout
        << "FINAL RESULT: FAIL
"
        << "At least one numerical or regression check failed.
";

    return 1;
}
